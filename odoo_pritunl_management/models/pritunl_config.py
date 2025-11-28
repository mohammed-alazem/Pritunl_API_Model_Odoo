# -*- coding: utf-8 -*-
import sys
import os
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

# Add lib directory to path
lib_path = os.path.join(os.path.dirname(__file__), '..', 'lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)


class PritunlConfig(models.Model):
    _name = 'pritunl.config'
    _description = 'Pritunl API Configuration'
    _rec_name = 'name'

    name = fields.Char('Configuration Name', required=True, default='Pritunl Server')
    base_url = fields.Char('Pritunl Server URL', required=True,
                           help="e.g., https://vpn1.craftron.co:8447")
    api_token = fields.Char('API Token', required=True,
                            help="Get this from Pritunl Admin panel")
    api_secret = fields.Char('API Secret', required=True,
                             help="Get this from Pritunl Admin panel")
    verify_ssl = fields.Boolean('Verify SSL', default=True,
                                help="Uncheck if using self-signed certificates")
    timeout = fields.Integer('Request Timeout (seconds)', default=30)
    active = fields.Boolean('Active', default=True)
    is_default = fields.Boolean('Is Default Configuration', default=False)

    # Statistics
    last_sync_date = fields.Datetime('Last Sync Date', readonly=True)
    sync_status = fields.Selection([
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('never', 'Never Synced')
    ], string='Last Sync Status', default='never', readonly=True)
    sync_message = fields.Text('Last Sync Message', readonly=True)

    _sql_constraints = [
        ('unique_default', 'CHECK(1=1)',
         'Only one default configuration is allowed!'),
    ]

    @api.constrains('is_default')
    def _check_default_config(self):
        """Ensure only one default configuration exists"""
        for record in self:
            if record.is_default:
                other_defaults = self.search([
                    ('is_default', '=', True),
                    ('id', '!=', record.id)
                ])
                if other_defaults:
                    raise ValidationError(
                        "Only one default configuration is allowed. "
                        f"'{other_defaults[0].name}' is already set as default."
                    )

    def get_client(self):
        """
        Get authenticated Pritunl API client

        Returns:
            PritunlAuth instance configured with this config
        """
        self.ensure_one()

        try:
            from auth import PritunlAuth

            client = PritunlAuth(
                base_url=self.base_url,
                api_token=self.api_token,
                api_secret=self.api_secret,
                verify_ssl=self.verify_ssl,
                timeout=self.timeout
            )
            return client
        except Exception as e:
            raise UserError(f"Failed to create Pritunl client: {str(e)}")

    @api.model
    def get_default_config(self):
        """Get the default configuration"""
        config = self.search([('is_default', '=', True), ('active', '=', True)], limit=1)
        if not config:
            config = self.search([('active', '=', True)], limit=1)
        if not config:
            raise UserError(
                "No Pritunl configuration found. "
                "Please configure Pritunl API credentials first."
            )
        return config

    def action_test_connection(self):
        """Test API connection"""
        self.ensure_one()

        try:
            from status import ping

            client = self.get_client()
            result = ping(client=client)

            self.write({
                'sync_status': 'success',
                'sync_message': 'Connection successful!',
                'last_sync_date': fields.Datetime.now()
            })

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Connection Successful',
                    'message': 'Successfully connected to Pritunl server!',
                    'type': 'success',
                    'sticky': False,
                }
            }
        except Exception as e:
            self.write({
                'sync_status': 'failed',
                'sync_message': str(e),
                'last_sync_date': fields.Datetime.now()
            })

            raise UserError(f"Connection failed: {str(e)}")

    def action_sync_all(self):
        """Synchronize all data from Pritunl"""
        self.ensure_one()

        try:
            # Sync organizations
            self.env['pritunl.organization'].action_sync_from_pritunl()

            # Sync servers
            self.env['pritunl.server'].action_sync_from_pritunl()

            # Sync hosts
            self.env['pritunl.host'].action_sync_from_pritunl()

            self.write({
                'sync_status': 'success',
                'sync_message': 'All data synchronized successfully',
                'last_sync_date': fields.Datetime.now()
            })

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sync Successful',
                    'message': 'All Pritunl data synchronized successfully!',
                    'type': 'success',
                    'sticky': False,
                }
            }
        except Exception as e:
            self.write({
                'sync_status': 'failed',
                'sync_message': str(e),
                'last_sync_date': fields.Datetime.now()
            })

            raise UserError(f"Synchronization failed: {str(e)}")

    @api.model
    def cron_sync_pritunl_data(self):
        """Scheduled action to sync Pritunl data"""
        configs = self.search([('active', '=', True)])
        for config in configs:
            try:
                config.action_sync_all()
            except Exception as e:
                # Log error but continue with other configs
                config.write({
                    'sync_status': 'failed',
                    'sync_message': str(e),
                    'last_sync_date': fields.Datetime.now()
                })
