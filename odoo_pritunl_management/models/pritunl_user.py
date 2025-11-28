# -*- coding: utf-8 -*-
import sys
import os
from odoo import models, fields, api
from odoo.exceptions import UserError

lib_path = os.path.join(os.path.dirname(__file__), '..', 'lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)


class PritunlUser(models.Model):
    _name = 'pritunl.user'
    _description = 'Pritunl VPN User'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    # Basic Info
    name = fields.Char('Username', required=True, tracking=True)
    email = fields.Char('Email', tracking=True)
    pin = fields.Char('PIN', help="User PIN for additional authentication")

    # Pritunl Info
    pritunl_id = fields.Char('Pritunl User ID', readonly=True, copy=False)
    organization_id = fields.Many2one('pritunl.organization', string='Organization',
                                      required=True, ondelete='cascade', tracking=True)
    config_id = fields.Related('organization_id.config_id', string='Configuration', store=True)

    # Partner Link (for subscription control)
    partner_id = fields.Many2one('res.partner', string='Related Partner',
                                 help="Link to customer for subscription control", tracking=True)

    # Subscription Control
    subscription_id = fields.Many2one('sale.subscription', string='Subscription',
                                     help="User's VPN subscription")
    subscription_state = fields.Selection(related='subscription_id.state',
                                         string='Subscription Status', store=True)

    # Status
    disabled = fields.Boolean('Disabled', default=False, tracking=True,
                             help="Disable user access")
    active = fields.Boolean('Active', default=True)
    synced = fields.Boolean('Synced with Pritunl', readonly=True, copy=False)

    # VPN Settings
    groups = fields.Char('Groups', help="Comma-separated group names")
    bypass_secondary = fields.Boolean('Bypass Secondary Auth', default=False)
    client_to_client = fields.Boolean('Client to Client', default=False,
                                     help="Allow client-to-client communication")
    dns_servers = fields.Char('DNS Servers', help="Comma-separated DNS servers")
    dns_suffix = fields.Char('DNS Suffix')

    # OTP
    otp_secret = fields.Char('OTP Secret', readonly=True)
    otp_auth_url = fields.Char('OTP Auth URL', readonly=True)

    # Audit
    last_sync_date = fields.Datetime('Last Sync Date', readonly=True)

    def _get_client(self):
        """Get Pritunl client from configuration"""
        return self.organization_id._get_client()

    def _prepare_pritunl_values(self):
        """Prepare values for Pritunl API"""
        self.ensure_one()

        values = {
            'name': self.name,
            'disabled': self.disabled,
            'bypass_secondary': self.bypass_secondary,
            'client_to_client': self.client_to_client,
        }

        if self.email:
            values['email'] = self.email
        if self.pin:
            values['pin'] = self.pin
        if self.groups:
            values['groups'] = [g.strip() for g in self.groups.split(',') if g.strip()]
        if self.dns_servers:
            values['dns_servers'] = [d.strip() for d in self.dns_servers.split(',') if d.strip()]
        if self.dns_suffix:
            values['dns_suffix'] = self.dns_suffix

        return values

    @api.model_create_multi
    def create(self, vals_list):
        """Create user in Pritunl when created in Odoo"""
        records = super().create(vals_list)

        for record in records:
            if not record.pritunl_id and record.organization_id.pritunl_id:
                try:
                    from users import create_user

                    client = record._get_client()
                    user_vals = record._prepare_pritunl_values()

                    user = create_user(
                        org_id=record.organization_id.pritunl_id,
                        client=client,
                        **user_vals
                    )

                    record.write({
                        'pritunl_id': user['id'],
                        'synced': True,
                        'last_sync_date': fields.Datetime.now()
                    })

                    record.message_post(
                        body=f"VPN user created in Pritunl with ID: {user['id']}"
                    )
                except Exception as e:
                    raise UserError(f"Failed to create user in Pritunl: {str(e)}")

        return records

    def write(self, vals):
        """Update user in Pritunl when updated in Odoo"""
        # Check if subscription state changed
        if 'subscription_state' in vals or 'subscription_id' in vals:
            self._handle_subscription_change()

        result = super().write(vals)

        # Update in Pritunl if relevant fields changed
        pritunl_fields = ['name', 'email', 'pin', 'disabled', 'groups',
                         'bypass_secondary', 'client_to_client', 'dns_servers', 'dns_suffix']

        if any(field in vals for field in pritunl_fields):
            for record in self.filtered(lambda r: r.pritunl_id):
                try:
                    from users import update_user

                    client = record._get_client()
                    user_vals = record._prepare_pritunl_values()

                    update_user(
                        org_id=record.organization_id.pritunl_id,
                        user_id=record.pritunl_id,
                        client=client,
                        **user_vals
                    )

                    record.write({
                        'synced': True,
                        'last_sync_date': fields.Datetime.now()
                    })

                    record.message_post(
                        body=f"VPN user updated in Pritunl"
                    )
                except Exception as e:
                    raise UserError(f"Failed to update user in Pritunl: {str(e)}")

        return result

    def unlink(self):
        """Delete user from Pritunl when deleted in Odoo"""
        for record in self:
            if record.pritunl_id and record.organization_id.pritunl_id:
                try:
                    from users import delete_user

                    client = record._get_client()
                    delete_user(
                        org_id=record.organization_id.pritunl_id,
                        user_id=record.pritunl_id,
                        client=client
                    )
                except Exception as e:
                    raise UserError(f"Failed to delete user from Pritunl: {str(e)}")

        return super().unlink()

    def _handle_subscription_change(self):
        """Handle subscription state changes"""
        for record in self:
            if record.subscription_id:
                # Disable user if subscription is not in progress
                if record.subscription_state not in ['progress', '3_progress']:
                    if not record.disabled:
                        record.disabled = True
                        record.message_post(
                            body=f"User disabled due to subscription status: {record.subscription_state}"
                        )
                # Enable user if subscription is in progress
                else:
                    if record.disabled:
                        record.disabled = False
                        record.message_post(
                            body="User enabled due to active subscription"
                        )

    def action_toggle_disable(self):
        """Toggle user disabled status"""
        for record in self:
            record.disabled = not record.disabled

    def action_generate_otp(self):
        """Generate new OTP secret for user"""
        self.ensure_one()

        if not self.pritunl_id:
            raise UserError("User not synced with Pritunl yet")

        try:
            from users import generate_otp_secret

            client = self._get_client()
            otp = generate_otp_secret(
                org_id=self.organization_id.pritunl_id,
                user_id=self.pritunl_id,
                client=client
            )

            self.write({
                'otp_secret': otp.get('secret'),
                'otp_auth_url': otp.get('otpauth_url')
            })

            self.message_post(
                body=f"OTP Secret generated: {otp.get('secret')}"
            )

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'OTP Generated',
                    'message': f"OTP Secret: {otp.get('secret')}",
                    'type': 'success',
                    'sticky': True,
                }
            }
        except Exception as e:
            raise UserError(f"Failed to generate OTP: {str(e)}")

    def action_download_vpn_config(self):
        """Download VPN configuration files"""
        self.ensure_one()

        if not self.pritunl_id:
            raise UserError("User not synced with Pritunl yet")

        try:
            from keys import get_user_key_urls

            client = self._get_client()
            key_urls = get_user_key_urls(
                org_id=self.organization_id.pritunl_id,
                user_id=self.pritunl_id,
                client=client
            )

            # Return action to open download URLs
            message = "VPN Configuration URLs:\n\n"
            for key, url in key_urls.items():
                message += f"{key}: {url}\n"

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'VPN Configuration',
                    'message': message,
                    'type': 'info',
                    'sticky': True,
                }
            }
        except Exception as e:
            raise UserError(f"Failed to get VPN configuration: {str(e)}")

    def action_sync_from_organization(self):
        """Sync users from Pritunl organization"""
        if not self.organization_id or not self.organization_id.pritunl_id:
            raise UserError("Organization not synced with Pritunl")

        try:
            from users import list_users

            client = self._get_client()
            pritunl_users = list_users(
                org_id=self.organization_id.pritunl_id,
                client=client
            )

            synced_count = 0
            for user_data in pritunl_users:
                existing = self.search([
                    ('pritunl_id', '=', user_data['id']),
                    ('organization_id', '=', self.organization_id.id)
                ], limit=1)

                if existing:
                    existing.write({
                        'name': user_data['name'],
                        'email': user_data.get('email'),
                        'disabled': user_data.get('disabled', False),
                        'synced': True,
                        'last_sync_date': fields.Datetime.now()
                    })
                else:
                    self.create({
                        'name': user_data['name'],
                        'email': user_data.get('email'),
                        'pritunl_id': user_data['id'],
                        'organization_id': self.organization_id.id,
                        'disabled': user_data.get('disabled', False),
                        'synced': True,
                        'last_sync_date': fields.Datetime.now()
                    })
                synced_count += 1

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sync Successful',
                    'message': f'Synchronized {synced_count} users from Pritunl',
                    'type': 'success',
                }
            }
        except Exception as e:
            raise UserError(f"Failed to sync users: {str(e)}")

    @api.model
    def cron_check_subscriptions(self):
        """Scheduled action to check subscription status and enable/disable users"""
        users = self.search([('subscription_id', '!=', False)])
        for user in users:
            user._handle_subscription_change()
