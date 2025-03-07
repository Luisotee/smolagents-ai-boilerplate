from smolagents.tools import Tool


class ClinicGeneralInfoTool(Tool):
    """Tool that provides general information about Clínica Bella."""

    name = "clinic_general_info"
    description = "Returns basic information about Clínica Bella, including location, contact details, and clinic overview."
    inputs = {}  # No inputs needed - just call the tool directly
    output_type = "string"

    def __init__(self):
        super().__init__()
        self.info = """
### About Clínica Bella
- Official name: Clínica Bella - Beauty and Wellness in Porto Alegre
- Location: Rua das Flores, 1234 - Belém Novo neighborhood, Porto Alegre - RS, 91787-000
- Contact: WhatsApp number: +55 51 99948-9818
- Phone: +55 51 99948-9818
- Email: contato@clinicabella.com.br
- Website: www.clinicabella.com.br
- Instagram: @clinicabella
- Developed by: cod3.team

### About the Clinic
Clínica Bella is a space dedicated to beauty and wellness, located in the heart of Porto Alegre, RS. 
Our mission is to provide high-quality aesthetic treatments with specialized professionals and state-of-the-art equipment. 
Our environment has been carefully designed to offer comfort and tranquility to our clients.

### Facility Structure
- 3 Procedure Rooms: Equipped with cutting-edge technology to ensure safety and efficacy.
- Comfortable Waiting Area: With sofas, magazines, and free Wi-Fi.
- Support Space: Bathrooms and resting area for clients.
- Private Parking: With free spots for clients.

### How to Get There
Clínica Bella is located at Rua das Flores, 1234, in the Belém Novo neighborhood, in Porto Alegre. 
We offer private parking for greater convenience of our clients.

### Clinic Differentials
- Personalized service with free evaluation
- State-of-the-art equipment
- Highly trained and certified professionals
- Sophisticated and comfortable environment
- Flexible payment plans
- Safe and sanitized environment, following all health protocols
- Personalized and humanized care
"""

    def forward(self):
        """Returns general information about Clínica Bella."""
        return self.info
