from smolagents.tools import Tool


class ClinicKnowledgeTool(Tool):
    """Tool that provides comprehensive information about Clínica Bella."""

    name = "clinic_knowledge"
    description = "Returns comprehensive information about Clínica Bella, including services, treatments, procedures, and policies."
    inputs = {}  # No inputs needed - just call the tool directly
    output_type = "string"

    def __init__(self):
        super().__init__()
        self.clinic_info = """
### About Clínica Bella
- Location: Porto Alegre, RS, in the Belém Novo neighborhood
- Contact: WhatsApp phone number: +55 51 99948-9818 (Only provide this to users when you're unable to answer their question or process their request)
- Developed by: cod3.team

### Treatments and Procedures
- Aesthetic treatments offered: facial cleansing, facial harmonization, Botox, lip filling, laser hair removal, microneedling, and more
- Botox: Botulinum toxin applications to reduce wrinkles and expression lines
- Lip filling: Performed with hyaluronic acid to give volume and contour to the lips, providing a natural and harmonious appearance
- Skin blemish treatments: Chemical peeling, microneedling, and laser

### Appointments and Operations
- Scheduling: Through WhatsApp, phone, or directly through Instagram
- Medical insurance: Not accepted, procedures are private but special payment conditions are available
- Operating hours: Monday to Friday, 9am to 7pm; Saturdays, 9am to 1pm

### Post-Procedure and Care
- Care after facial procedures: Avoid sun exposure, massages in the area, and intense physical effort in the first 24 hours
- Chemical peeling effects: Normal for skin to peel in the days following the procedure, part of the cell renewal process
"""

    def forward(self):
        """
        Returns the comprehensive clinic information.

        Returns:
            A string containing the comprehensive information about Clínica Bella
        """
        # Return the full clinic information
        return self.clinic_info
