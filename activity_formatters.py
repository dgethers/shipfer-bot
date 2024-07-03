class ShipmentFormatter:

    @staticmethod
    def format_shipments_to_markdown(shipments) -> str:
        tokens = []
        for shipment in shipments:
            tokens.append(f'**{shipment["shipmentId"]}**')
            tokens.append(f' *status: {shipment["status"]}*')
            to_address = shipment["toAddress"]
            tokens.append(f' {ShipmentFormatter._format_shipment_address(to_address)} ')

        return ''.join(tokens)

    @staticmethod
    def _format_shipment_address(shipment_address):
        address_parts = []
        if shipment_address["residential"]:
            address_parts.append(shipment_address['name'])
        else:
            address_parts.append(shipment_address['company'])

        address_parts.append(shipment_address["addressLine1"])

        if shipment_address["addressLine2"]:
            address_parts.append(shipment_address["addressLine2"])
        if shipment_address["addressLine3"]:
            address_parts.append(shipment_address["addressLine3"])

        address_parts.extend([
            shipment_address["cityTown"],
            shipment_address["stateProvince"],
            shipment_address["postalCode"]
        ])

        if not shipment_address["residential"]:
            address_parts.insert(0, shipment_address["company"])

        return ', '.join(address_parts)
