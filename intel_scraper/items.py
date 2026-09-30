import scrapy


class XeonItem(scrapy.Item):
    pass


XeonItem.fields.update({

    "product_name": scrapy.Field(),

    "Launch Date": scrapy.Field(),
    "Total Cores": scrapy.Field(),
    "Max Turbo Frequency": scrapy.Field(),
    "Processor Base Frequency": scrapy.Field(),
    "Cache": scrapy.Field(),
    "TDP": scrapy.Field(),

    "category": scrapy.Field(),
    "product_family": scrapy.Field(),
    "product_line": scrapy.Field(),
    "vertical_segment": scrapy.Field(),
    "processor_number": scrapy.Field(),

    "maximum_memory_channels": scrapy.Field(),
    "maximum_memory_size": scrapy.Field(),
    "memory_type": scrapy.Field(),
    "maximum_memory_speed": scrapy.Field(),
    "ECC_memory_supported": scrapy.Field(),

    "product_specification": scrapy.Field(),
    "compliance_description": scrapy.Field(),
    "specification_code": scrapy.Field(),
    "ordering_code": scrapy.Field(),

    "url": scrapy.Field(),
    "store": scrapy.Field(),
})