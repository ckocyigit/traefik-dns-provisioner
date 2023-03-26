# coding: utf-8

# flake8: noqa

"""
    DNS API

    ## Working with the API Every endpoint uses the `X-API-Key` header for authorization, to obtain the key please see the [Official Documentation](/docs/getstarted).  Please note that any zone or record updates might conflict with active services. In such cases, the DNS records belonging to the conflicting services will be deactivated.  ## Support Support questions may be posted in English: <a href='/docs/getstarted#support'>API Support</a>.  Please note that we offer support in the business Hours Mo-Fri 9:00-17:00 EET. <h2> <details>   <summary>Release notes</summary>   <ul>     <li>Version 1.0.0 Exposed CRUD operations for customer zone.</li>     <li>Version 1.0.1 Added response body for UPDATE and CREATE record operations.</li>     <li>Version 1.0.2 Added new supported record types.</li>   </ul> </details> </h2>   # noqa: E501

    OpenAPI spec version: 1.0.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

# import apis into sdk package
from ionos.api.dynamic_dns_api import DynamicDNSApi
from ionos.api.records_api import RecordsApi
from ionos.api.zones_api import ZonesApi
# import ApiClient
from ionos.api_client import ApiClient
from ionos.configuration import Configuration
# import models into sdk package
from ionos.models.customer_zone import CustomerZone
from ionos.models.dyn_dns_request import DynDnsRequest
from ionos.models.dynamic_dns import DynamicDns
from ionos.models.error import Error
from ionos.models.errors import Errors
from ionos.models.errors_inner import ErrorsInner
from ionos.models.record import Record
from ionos.models.record_response import RecordResponse
from ionos.models.record_types import RecordTypes
from ionos.models.record_update import RecordUpdate
from ionos.models.zone import Zone
from ionos.models.zone_types import ZoneTypes