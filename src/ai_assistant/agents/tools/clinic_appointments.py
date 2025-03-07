from smolagents.tools import Tool


class ClinicAppointmentsTool(Tool):
    """Tool that provides information about appointments and policies at Clínica Bella."""

    name = "clinic_appointments"
    description = "Returns information about scheduling, cancellation policies, and appointment procedures at Clínica Bella."
    inputs = {}
    output_type = "string"

    def __init__(self):
        super().__init__()
        self.appointments_info = """
### Appointments and Operational Information

#### Operating Hours
- Monday to Friday: 9am to 7pm
- Saturday: 9am to 1pm
- Sunday: Closed
- Holidays: Limited hours, please check our Instagram or website

#### Scheduling Options
- WhatsApp: +55 51 99948-9818
- Phone: +55 51 99948-9818
- Email: agendamentos@clinicabella.com.br
- Website: www.clinicabella.com.br/agendar

#### Appointment Procedures
- First-time clients receive a complimentary consultation
- Arrive 15 minutes before your appointment for registration
- Medical procedures require an initial consultation with our physicians
- Digital forms will be sent prior to your appointment to save time

#### Policies
- Medical insurance is not accepted, all procedures are private pay
- Special payment conditions and installment plans are available
- 24-hour cancellation notice required
- Late cancellations or no-shows may incur a rebooking fee
- Rescheduling is subject to availability

#### Pre and Post Care
- Specific instructions will be provided before your procedure
- General care after facial procedures: Avoid sun exposure, massages in the area, 
  and intense physical effort in the first 24 hours
- Chemical peeling effects: Normal for skin to peel in the days following the procedure, 
  part of the cell renewal process
- Follow-up appointments are scheduled as needed based on your treatment plan
"""

    def forward(self):
        """Returns information about appointments and policies."""
        return self.appointments_info
