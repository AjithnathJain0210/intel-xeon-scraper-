import scrapy
import json


class XeonSpider(scrapy.Spider):

    name = "xeon"

    # Starting point: Intel Xeon 6 Series page
    start_urls = [
        "https://www.intel.com/content/www/us/en/ark/products/series/240357/intel-xeon-6-processors.html"
    ]

    def parse(self, response):

        # We are currently on the Xeon 6 Series page.
        # Find all links that point to individual product pages.
        product_links = response.css(
            'a[href*="/products/sku/"]::attr(href)'
        ).getall()

        print("Total Product Links:", len(product_links))

        # Skip the first 29 products.
        # Select the remaining 62 products.
        product_links = product_links[29:]

        print("Products Selected:", len(product_links))

        # Check for duplicate product links
        unique_product_links = set(product_links)

        print("Unique Products:", len(unique_product_links))

        if len(product_links) != len(unique_product_links):

            print("DUPLICATE PRODUCT LINK FOUND")

            seen = set()

            for link in product_links:

                if link in seen:
                    print("DUPLICATE:", link)

                else:
                    seen.add(link)

        # Navigate to each Product Detail page.
        for link in product_links:

            yield response.follow(
                link,
                callback=self.parse_product
            )


    def parse_product(self, response):

        print("PRODUCT PAGE REACHED:", response.url)

        # 1. Product Name
        product_name = response.css("h1::text").get()

        # 2. Launch Date
        launch_date = response.xpath(
            '//div[@class="row-key" and normalize-space()="Launch Date"]'
            '/ancestor::tr'
            '//div[contains(@class, "row-value")]'
        ).xpath("normalize-space()").get()

        # 3. Total Cores
        total_cores = response.xpath(
            '//div[@class="row-key" and normalize-space()="Total Cores"]'
            '/ancestor::tr'
            '//div[contains(@class, "row-value")]'
        ).xpath("normalize-space()").get()

        # 4. Max Turbo Frequency
        max_turbo_frequency = response.xpath(
            '//div[@class="row-key" and normalize-space()="Max Turbo Frequency"]'
            '/ancestor::tr'
            '//div[contains(@class, "row-value")]'
        ).xpath("normalize-space()").get()

        if max_turbo_frequency and "GHz" not in max_turbo_frequency:
            max_turbo_frequency = max_turbo_frequency + " GHz"

        # 5. Processor Base Frequency
        processor_base_frequency = response.xpath(
            '//div[@class="row-key" and normalize-space()="Processor Base Frequency"]'
            '/ancestor::tr'
            '//div[contains(@class, "row-value")]'
        ).xpath("normalize-space()").get()

        if processor_base_frequency and "GHz" not in processor_base_frequency:
            processor_base_frequency = processor_base_frequency + " GHz"

        # 6. Cache
        cache = response.xpath(
            '//div[@class="row-key" and normalize-space()="Cache"]'
            '/ancestor::tr'
            '//div[contains(@class, "row-value")]'
        ).xpath("normalize-space()").get()

        # 7. TDP
        tdp = response.xpath(
            '//div[@class="row-key" and normalize-space()="TDP"]'
            '/ancestor::tr'
            '//div[contains(@class, "row-value")]'
        ).xpath("normalize-space()").get()

        if tdp and "W" not in tdp:
            tdp = tdp + " W"

        # 8. Category
        category = "processor"

        # 9. Product Family
        product_family = response.xpath(
            '//div[@class="row-key" and normalize-space()="Product Collection"]'
            '/ancestor::tr'
            '//div[contains(@class, "row-value")]'
        ).xpath("normalize-space()").get()

        # 10. Product Line
        product_line = response.xpath(
            '//div[@class="row-key" and normalize-space()="Code Name"]'
            '/ancestor::tr'
            '//div[contains(@class, "row-value")]'
        ).xpath("normalize-space()").get()

        # 11. Vertical Segment
        vertical_segment = response.xpath(
            '//div[@class="row-key" and normalize-space()="Vertical Segment"]'
            '/ancestor::tr'
            '//div[contains(@class, "row-value")]'
        ).xpath("normalize-space()").get()

        # 12. Processor Number
        processor_number = response.xpath(
            '//div[@class="row-key" and normalize-space()="Processor Number"]'
            '/ancestor::tr'
            '//div[contains(@class, "row-value")]'
        ).xpath("normalize-space()").get()

        # 13. Maximum Memory Channels
        maximum_memory_channels = response.xpath(
            '//div[@class="row-key" and normalize-space()="Max # of Memory Channels"]'
            '/ancestor::tr'
            '//div[contains(@class, "row-value")]'
        ).xpath("normalize-space()").get()

        # 14. Maximum Memory Size
        maximum_memory_size = response.xpath(
            '//div[@class="row-key" and normalize-space()="Max Memory Size (dependent on memory type)"]'
            '/ancestor::tr'
            '//div[contains(@class, "row-value")]'
        ).xpath("normalize-space()").get()

        # 15. Memory Type
        memory_type = response.xpath(
            '//div[@class="row-key" and normalize-space()="Memory Types"]'
            '/ancestor::tr'
            '//div[contains(@class, "row-value")]'
        ).xpath("normalize-space()").get()

        # 16. Maximum Memory Speed
        maximum_memory_speed = response.xpath(
            '//div[@class="row-key" and normalize-space()="Maximum Memory Speed"]'
            '/ancestor::tr'
            '//div[contains(@class, "row-value")]'
        ).xpath("normalize-space()").get()

        # Convert Intel's MT/s format to the sample's MHz format
        if maximum_memory_speed:
            maximum_memory_speed = maximum_memory_speed.replace(
                " MT/s",
                ""
            )

            if "MHz" not in maximum_memory_speed:
                maximum_memory_speed = maximum_memory_speed + " MHz"

        # 17. ECC Memory Supported
        ecc_memory_supported = response.xpath(
            '//div[@class="row-key" and contains(normalize-space(), "ECC Memory Supported")]'
            '/ancestor::tr'
            '//div[contains(@class, "row-value")]'
        ).xpath("normalize-space()").get()

        # 18. Product Specification
        product_specification = {}

        spec_rows = response.xpath(
            '//div[contains(@class, "row-key")]/ancestor::tr'
        )

        for row in spec_rows:

            key = row.xpath(
                './/div[contains(@class, "row-key")]'
            ).xpath("normalize-space()").get()

            value = row.xpath(
                './/div[contains(@class, "row-value")]'
            ).xpath("normalize-space()").get()

            if key and value:

                if key == "Max Turbo Frequency" and "GHz" not in value:
                    value = value + " GHz"

                elif key == "Processor Base Frequency" and "GHz" not in value:
                    value = value + " GHz"

                elif key == "TDP" and "W" not in value:
                    value = value + " W"

                elif key == "Maximum Memory Speed":

                    value = value.replace(
                        " MT/s",
                        ""
                    )

                    if "MHz" not in value:
                        value = value + " MHz"

                product_specification[key] = [value]

        # Convert dictionary into JSON
        product_specification = json.dumps(
            product_specification,
            ensure_ascii=False
        )

        # Print extracted values
        print("----------------------------------------")
        print("PRODUCT RESPONSE:", response.url)
        print("----------------------------------------")

        print("Product Name:", product_name)
        print("Launch Date:", launch_date)
        print("Total Cores:", total_cores)
        print("Max Turbo Frequency:", max_turbo_frequency)
        print("Processor Base Frequency:", processor_base_frequency)
        print("Cache:", cache)
        print("TDP:", tdp)
        print("Category:", category)
        print("Product Family:", product_family)
        print("Product Line:", product_line)
        print("Vertical Segment:", vertical_segment)
        print("Processor Number:", processor_number)
        print("Maximum Memory Channels:", maximum_memory_channels)
        print("Maximum Memory Size:", maximum_memory_size)
        print("Memory Type:", memory_type)
        print("Maximum Memory Speed:", maximum_memory_speed)
        print("ECC Memory Supported:", ecc_memory_supported)
        print("Product Specification:", product_specification)

        # 22. URL
        url = response.url
        print("URL:", url)

        # 23. Store
        store = "Intel"
        print("Store:", store)

        # Navigate to Ordering & Compliance page
        ordering_url = response.url.replace(
            "/specifications.html",
            "/ordering.html"
        )

        # Carry Product page data to Ordering page
        yield response.follow(
            ordering_url,
            callback=self.parse_ordering,
            meta={
                "product_name": product_name,
                "launch_date": launch_date,
                "total_cores": total_cores,
                "max_turbo_frequency": max_turbo_frequency,
                "processor_base_frequency": processor_base_frequency,
                "cache": cache,
                "tdp": tdp,
                "category": category,
                "product_family": product_family,
                "product_line": product_line,
                "vertical_segment": vertical_segment,
                "processor_number": processor_number,
                "maximum_memory_channels": maximum_memory_channels,
                "maximum_memory_size": maximum_memory_size,
                "memory_type": memory_type,
                "maximum_memory_speed": maximum_memory_speed,
                "ecc_memory_supported": ecc_memory_supported,
                "product_specification": product_specification,
                "url": url,
                "store": store
            },
            dont_filter=True
        )


    def parse_ordering(self, response):

        # DEBUG: Check Ordering page response
        print("ORDERING PAGE REACHED:", response.url)
        print("STATUS:", response.status)

        # 19. Compliance Description
        compliance_description = response.css(
            "h3.cmp-title__text::text"
        ).get()

        # 20. Specification Code
        specification_codes = response.xpath(
            '//div[@class="row-key" and normalize-space()="Spec Code"]'
            '/ancestor::tr'
            '//td[contains(@class, "value")]'
        ).xpath("normalize-space()").getall()

        specification_code = ", ".join(
            specification_codes
        )

        # 21. Ordering Code
        ordering_codes = response.xpath(
            '//div[@class="row-key" and normalize-space()="Ordering Code"]'
            '/ancestor::tr'
            '//td[contains(@class, "value")]'
        ).xpath("normalize-space()").getall()

        ordering_code = ", ".join(
            ordering_codes
        )

    
        print("ORDERING RESPONSE:", response.url)
        

        print("Compliance Description:", compliance_description)
        print("Specification Code:", specification_code)
        print("Ordering Code:", ordering_code)

        # Get Product page values from meta
        product_name = response.meta["product_name"]
        launch_date = response.meta["launch_date"]
        total_cores = response.meta["total_cores"]
        max_turbo_frequency = response.meta["max_turbo_frequency"]
        processor_base_frequency = response.meta["processor_base_frequency"]
        cache = response.meta["cache"]
        tdp = response.meta["tdp"]
        category = response.meta["category"]
        product_family = response.meta["product_family"]
        product_line = response.meta["product_line"]
        vertical_segment = response.meta["vertical_segment"]
        processor_number = response.meta["processor_number"]
        maximum_memory_channels = response.meta["maximum_memory_channels"]
        maximum_memory_size = response.meta["maximum_memory_size"]
        memory_type = response.meta["memory_type"]
        maximum_memory_speed = response.meta["maximum_memory_speed"]
        ecc_memory_supported = response.meta["ecc_memory_supported"]
        product_specification = response.meta["product_specification"]
        url = response.meta["url"]
        store = response.meta["store"]

        # Create the final item containing all 23 columns
        item = {
            "product_name": product_name,
            "Launch Date": launch_date,
            "Total Cores": total_cores,
            "Max Turbo Frequency": max_turbo_frequency,
            "Processor Base Frequency": processor_base_frequency,
            "Cache": cache,
            "TDP": tdp,
            "category": category,
            "product_family": product_family,
            "product_line": product_line,
            "vertical_segment": vertical_segment,
            "processor_number": processor_number,
            "maximum_memory_channels": maximum_memory_channels,
            "maximum_memory_size": maximum_memory_size,
            "memory_type": memory_type,
            "maximum_memory_speed": maximum_memory_speed,
            "ECC_memory_supported": ecc_memory_supported,
            "product_specification": product_specification,
            "compliance_description": compliance_description,
            "specification_code": specification_code,
            "ordering_code": ordering_code,
            "url": url,
            "store": store
        }

        print("FINAL ITEM CREATED:", product_name)

        yield item