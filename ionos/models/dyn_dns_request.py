# coding: utf-8

"""
    DNS API

    ## Working with the API Every endpoint uses the `X-API-Key` header for authorization, to obtain the key please see the [Official Documentation](/docs/getstarted).  Please note that any zone or record updates might conflict with active services. In such cases, the DNS records belonging to the conflicting services will be deactivated.  ## Support Support questions may be posted in English: <a href='/docs/getstarted#support'>API Support</a>.  Please note that we offer support in the business Hours Mo-Fri 9:00-17:00 EET. <h2> <details>   <summary>Release notes</summary>   <ul>     <li>Version 1.0.0 Exposed CRUD operations for customer zone.</li>     <li>Version 1.0.1 Added response body for UPDATE and CREATE record operations.</li>     <li>Version 1.0.2 Added new supported record types.</li>   </ul> </details> </h2>   # noqa: E501

    OpenAPI spec version: 1.0.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class DynDnsRequest(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'domains': 'list[str]',
        'description': 'str'
    }

    attribute_map = {
        'domains': 'domains',
        'description': 'description'
    }

    def __init__(self, domains=None, description=None):  # noqa: E501
        """DynDnsRequest - a model defined in Swagger"""  # noqa: E501
        self._domains = None
        self._description = None
        self.discriminator = None
        self.domains = domains
        if description is not None:
            self.description = description

    @property
    def domains(self):
        """Gets the domains of this DynDnsRequest.  # noqa: E501


        :return: The domains of this DynDnsRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._domains

    @domains.setter
    def domains(self, domains):
        """Sets the domains of this DynDnsRequest.


        :param domains: The domains of this DynDnsRequest.  # noqa: E501
        :type: list[str]
        """
        if domains is None:
            raise ValueError("Invalid value for `domains`, must not be `None`")  # noqa: E501

        self._domains = domains

    @property
    def description(self):
        """Gets the description of this DynDnsRequest.  # noqa: E501

        Dynamic Dns description.  # noqa: E501

        :return: The description of this DynDnsRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this DynDnsRequest.

        Dynamic Dns description.  # noqa: E501

        :param description: The description of this DynDnsRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(DynDnsRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, DynDnsRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
