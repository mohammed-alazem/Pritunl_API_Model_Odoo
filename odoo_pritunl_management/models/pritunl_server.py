# -*- coding: utf-8 -*-
import sys
import os
from odoo import models, fields, api
from odoo.exceptions import UserError

lib_path = os.path.join(os.path.dirname(__file__), '..', 'lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)


class PritunlServer(models.Model):
    _name = 'pritunl.server'
    _description = 'Pritunl VPN Server'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    # Basic Info
    name = fields.Char('Server Name', required=True, tracking=True)
    pritunl_id = fields.Char('Pritunl Server ID', readonly=True, copy=False)
    config_id = fields.Many2one('pritunl.config', string='Configuration',
                                default=lambda self: self.env['pritunl.config'].get_default_config())

    # Network Configuration
    network = fields.Char('Network', required=True, default='10.0.0.0/8',
                         help="Network CIDR (e.g., 10.0.0.0/8)")
    network_start = fields.Char('Network Start IP')
    network_end = fields.Char('Network End IP')
    port = fields.Integer('Port', default=15500, tracking=True)
    protocol = fields.Selection([
        ('udp', 'UDP'),
        ('tcp', 'TCP'),
        ('udp6', 'UDP6'),
        ('tcp6', 'TCP6')
    ], string='Protocol', default='udp', required=True)

    # DNS Configuration
    dns_servers = fields.Char('DNS Servers', help="Comma-separated DNS servers")
    search_domain = fields.Char('Search Domain')

    # Server Settings
    max_clients = fields.Integer('Max Clients', default=2048)
    max_devices = fields.Integer('Max Devices per User', default=1)
    otp_auth = fields.Boolean('Require OTP', default=False)
    inter_client = fields.Boolean('Inter-Client Communication', default=True)
    ipv6 = fields.Boolean('Enable IPv6', default=False)
    ipv6_firewall = fields.Boolean('IPv6 Firewall', default=True)
    debug = fields.Boolean('Debug Mode', default=False)

    # Status
    status = fields.Selection([
        ('offline', 'Offline'),
        ('online', 'Online')
    ], string='Status', default='offline', readonly=True, tracking=True)
    active = fields.Boolean('Active', default=True)
    synced = fields.Boolean('Synced with Pritunl', readonly=True, copy=False)

    # Relations
    organization_ids = fields.Many2many('pritunl.organization', string='Organizations')

    def _get_client(self):
        """Get Pritunl client from configuration"""
        if self.config_id:
            return self.config_id.get_client()
        return self.env['pritunl.config'].get_default_config().get_client()

    @api.model_create_multi
    def create(self, vals_list):
        """Create server in Pritunl when created in Odoo"""
        records = super().create(vals_list)

        for record in records:
            if not record.pritunl_id:
                try:
                    from servers import create_server

                    client = record._get_client()

                    dns_list = []
                    if record.dns_servers:
                        dns_list = [d.strip() for d in record.dns_servers.split(',') if d.strip()]

                    server = create_server(
                        name=record.name,
                        network=record.network,
                        port=record.port,
                        protocol=record.protocol,
                        max_clients=record.max_clients,
                        max_devices=record.max_devices,
                        otp_auth=record.otp_auth,
                        inter_client=record.inter_client,
                        ipv6=record.ipv6,
                        ipv6_firewall=record.ipv6_firewall,
                        debug=record.debug,
                        dns_servers=dns_list if dns_list else None,
                        search_domain=record.search_domain or None,
                        client=client
                    )

                    record.write({
                        'pritunl_id': server['id'],
                        'synced': True
                    })

                    record.message_post(body=f"Server created in Pritunl with ID: {server['id']}")
                except Exception as e:
                    raise UserError(f"Failed to create server in Pritunl: {str(e)}")

        return records

    def action_start_server(self):
        """Start VPN server"""
        self.ensure_one()
        if not self.pritunl_id:
            raise UserError("Server not synced with Pritunl yet")

        try:
            from servers import start_server
            client = self._get_client()
            start_server(server_id=self.pritunl_id, client=client)

            self.write({'status': 'online'})
            self.message_post(body="Server started successfully")

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Server Started',
                    'message': f'{self.name} started successfully',
                    'type': 'success',
                }
            }
        except Exception as e:
            raise UserError(f"Failed to start server: {str(e)}")

    def action_stop_server(self):
        """Stop VPN server"""
        self.ensure_one()
        if not self.pritunl_id:
            raise UserError("Server not synced with Pritunl yet")

        try:
            from servers import stop_server
            client = self._get_client()
            stop_server(server_id=self.pritunl_id, client=client)

            self.write({'status': 'offline'})
            self.message_post(body="Server stopped successfully")

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Server Stopped',
                    'message': f'{self.name} stopped successfully',
                    'type': 'warning',
                }
            }
        except Exception as e:
            raise UserError(f"Failed to stop server: {str(e)}")

    def action_restart_server(self):
        """Restart VPN server"""
        self.ensure_one()
        if not self.pritunl_id:
            raise UserError("Server not synced with Pritunl yet")

        try:
            from servers import restart_server
            client = self._get_client()
            restart_server(server_id=self.pritunl_id, client=client)

            self.message_post(body="Server restarted successfully")

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Server Restarted',
                    'message': f'{self.name} restarted successfully',
                    'type': 'info',
                }
            }
        except Exception as e:
            raise UserError(f"Failed to restart server: {str(e)}")

    def action_attach_organizations(self):
        """Attach selected organizations to server"""
        self.ensure_one()
        if not self.pritunl_id:
            raise UserError("Server not synced with Pritunl yet")

        try:
            from servers import attach_organization
            client = self._get_client()

            for org in self.organization_ids:
                if org.pritunl_id:
                    attach_organization(
                        server_id=self.pritunl_id,
                        org_id=org.pritunl_id,
                        client=client
                    )

            self.message_post(body=f"Attached {len(self.organization_ids)} organizations")

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Organizations Attached',
                    'message': f'Attached {len(self.organization_ids)} organizations to server',
                    'type': 'success',
                }
            }
        except Exception as e:
            raise UserError(f"Failed to attach organizations: {str(e)}")

    @api.model
    def action_sync_from_pritunl(self):
        """Sync servers from Pritunl to Odoo"""
        try:
            from servers import list_servers

            config = self.env['pritunl.config'].get_default_config()
            client = config.get_client()

            pritunl_servers = list_servers(client=client)

            for server_data in pritunl_servers:
                existing = self.search([('pritunl_id', '=', server_data['id'])], limit=1)

                if existing:
                    existing.write({
                        'name': server_data['name'],
                        'status': server_data.get('status', 'offline'),
                        'synced': True
                    })
                else:
                    self.create({
                        'name': server_data['name'],
                        'pritunl_id': server_data['id'],
                        'network': server_data.get('network', '10.0.0.0/8'),
                        'port': server_data.get('port', 15500),
                        'protocol': server_data.get('protocol', 'udp'),
                        'status': server_data.get('status', 'offline'),
                        'config_id': config.id,
                        'synced': True
                    })

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sync Successful',
                    'message': f'Synchronized {len(pritunl_servers)} servers from Pritunl',
                    'type': 'success',
                }
            }
        except Exception as e:
            raise UserError(f"Failed to sync servers: {str(e)}")
