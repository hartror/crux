from __future__ import absolute_import

import logging
from cliff.command import Command

from ..exc import *


class TenantCreate(Command):

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(TenantCreate, self).get_parser(prog_name)

        parser.add_argument('--tenant-name', '--tenant', '-n')
        parser.add_argument('--tenant-description', '-d')
        parser.add_argument('--enabled',
                            action='store_true',
                            default=True)
        parser.add_argument('--disabled',
                            action='store_false',
                            dest='enabled')
        parser.add_argument('--update',
                            action='store_true')
        return parser

    def take_action(self, args):
        if not args.tenant_name:
            raise CruxException('you must provide a value for --tenant-name')

        self.find_or_create_tenant(args)

    def find_or_create_tenant(self, args):
        client = self.app.client
        tenants = client.tenants.list()

        res = [x for x in tenants if x.name == args.tenant_name]

        if res:
            tenant = res[0]
            self.log.info('using existing tenant %s (%s)',
                     tenant.name, tenant.id)

            if args.update:
                self.log.info('updating enabled=%s for tenant %s',
                              args.enabled, tenant.name)
                client.tenants.update(tenant.id,
                                      enabled=args.enabled)
                if args.tenant_description:
                    self.log.info('updating description for tenant %s',
                                  tenant.name)
                    client.tenants.update(tenant.id,
                                          description=args.tenant_description)
        else:
            tenant = client.tenants.create(
                args.tenant_name,
                description=args.tenant_description,
                enabled=args.enabled,
            )
            self.log.info('created tenant %s (%s)',
                          tenant.name, tenant.id)

        return tenant

