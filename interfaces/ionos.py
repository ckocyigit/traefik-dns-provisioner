from datetime import datetime
from ionos.api.dynamic_dns_api import DynamicDNSApi
from ionos.api.zones_api import ZonesApi
from ionos.api.records_api import RecordsApi
from ionos.models.dyn_dns_request import DynDnsRequest
from ionos.api_client import ApiClient
from ionos.configuration import Configuration

class Ionos():

    def __init__(self, token):
        apiClient_configuration = Configuration()
        apiClient_configuration.api_key = {'X-API-Key': token}
        apiClient = ApiClient(configuration=apiClient_configuration)

        self.dynamicAPI = DynamicDNSApi(api_client=apiClient)
        self.zonesAPI = ZonesApi(api_client=apiClient)
        self.recordsAPI = RecordsApi(api_client=apiClient)

    def register_domains(self, domains, description = f"Updated By TDP at {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"):
        dnsreq = DynDnsRequest(domains=domains, description=description)
        response = self.dynamicAPI.activate_dyn_dns(dnsreq)
        return response

    def getZoneID(self, targetDomain):
        for domain in self.zonesAPI.get_zones():
            if domain.name == targetDomain:
                return domain.id

    def getRecords(self, targetDomain, type = 'A'):
        records = []
        for record in self.zonesAPI.get_zone(self.getZoneID(targetDomain)).records:
            if record.type == type:
                records.append(record)
        return records

    def getRecordNames(self, targetDomain):
        """getRecordNames

        returns all records by name and id as tuple
        """           
        names = {}
        for record in self.getRecords(targetDomain):
            names.update({record.name: record.id})
        return names

    def deleteRecord(self, zoneid, recordid):
        self.recordsAPI.delete_record(zoneid,recordid)