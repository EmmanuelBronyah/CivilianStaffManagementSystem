import EmployeeInput from "./EmployeeInput/EmployeeInput";
import OccurrenceInput from "./OccurrenceInput/OccurrenceInput";
import ChildrenInput from "./ChildrenInput/ChildrenInput";
import SpouseInput from "./SpouseInput/SpouseInput";
import CourseInput from "./CourseInput/CourseInput";
import IdentityInput from "./IdentityInput/IdentityInput";
import NextOfKinInput from "./NextOfKinInput/NextOfKinInput";
import PreviousGovernmentServiceInput from "./PreviousGovernmentServiceInput/PreviousGovernmentServiceInput";
import ServiceWithForcesInput from "./ServiceWithForcesInput/ServiceWithForcesInput";
import TerminationOfAppointmentInput from "./TerminationOfAppointmentInput/TerminationOfAppointmentInput";

export const components = {
  Employee: EmployeeInput,
  Occurrence: OccurrenceInput,
  Children: ChildrenInput,
  Course: CourseInput,
  Identity: IdentityInput,
  Spouse: SpouseInput,
  "Emergency | Next of Kin": NextOfKinInput,
  "Previous Government Service": PreviousGovernmentServiceInput,
  "Service With Forces": ServiceWithForcesInput,
  "Termination of Appointment": TerminationOfAppointmentInput,
};

export const employeeLabels = [
  ["Service ID", "text", "input"],
  ["Last Name", "text", "input"],
  ["Other Names", "text", "input"],

  ["SSNIT Number", "text", "input"],
  ["Category", "text", "input"],
  ["Appointment Date", "date", "input"],

  ["Confirmation Date", "date", "input"],
  ["Probation", "number", "input"],
  ["Entry Qualification", "text", "input"],

  ["Unit", "text", "dropdown"],
  ["Grade", "text", "dropdown"],
  ["Station", "text", "input"],

  ["Date of Birth", "date", "input"],
  ["Age", "number", "input"],
  ["Gender", "text", "dropdown"],

  ["Hometown", "text", "input"],
  ["Region", "text", "dropdown"],
  ["Nationality", "text", "input"],

  ["Address", "text", "input"],
  ["Email", "email", "input"],
  ["Marital Status", "text", "dropdown"],

  ["Religion", "text", "dropdown"],
  ["Structure", "text", "dropdown"],
  ["Blood Group", "text", "dropdown"],

  ["Disable", "checkbox", "input"],

  ["Created By", "text", "dropdown"],
  ["Updated By", "text", "dropdown"],

  ["Date Added", "date", "input"],
  ["Date Modified", "date", "input"],
];

export const occurrenceLabels = [
  ["Grade", "text", "dropdown"],
  ["Authority", "text", "input"],
  ["LevelStep", "text", "dropdown"],
  ["Monthly Salary", "number", "input"],
  ["Annual Salary", "number", "input"],
  ["Event", "text", "dropdown"],
  ["Percentage", "number", "dropdown"],
  ["WEF Date", "date", "input"],
  ["Reason", "text", "input"],
  ["Created By", "text", "dropdown"],
  ["Updated By", "text", "dropdown"],
  ["Date Added", "date", "input"],
  ["Date Modified", "date", "input"],
];

export const childrenLabels = [
  ["Child Name", "text", "input"],
  ["Date of Birth", "date", "input"],
  ["Gender", "text", "dropdown"],
  ["Other Parent", "text", "input"],
  ["Authority", "text", "input"],
  ["Created By", "text", "dropdown"],
  ["Updated By", "text", "dropdown"],
  ["Date Added", "date", "input"],
  ["Date Modified", "date", "input"],
];

export const courseLabels = [
  ["Course Type", "text", "input"],
  ["Place", "text", "input"],
  ["From", "date", "input"],
  ["To", "date", "input"],
  ["Qualification", "text", "input"],
  ["Result", "text", "input"],
  ["Authority", "text", "input"],
  ["Created By", "text", "dropdown"],
  ["Updated By", "text", "dropdown"],
  ["Date Added", "date", "input"],
  ["Date Modified", "date", "input"],
];

export const identityLabels = [
  ["Voters ID", "text", "input"],
  ["National ID", "text", "input"],
  ["GLICO ID", "text", "input"],
  ["NHIS ID", "text", "input"],
  ["TIN Number", "text", "input"],
  ["Created By", "text", "dropdown"],
  ["Updated By", "text", "dropdown"],
  ["Date Added", "date", "input"],
  ["Date Modified", "date", "input"],
];

export const spouseLabels = [
  ["Spouse Name", "text", "input"],
  ["Phone Number", "tel", "input"],
  ["Address", "text", "input"],
  ["Registration Number", "text", "input"],
  ["Marriage Date", "date", "input"],
  ["Marriage Place", "text", "input"],
  ["Created By", "text", "dropdown"],
  ["Updated By", "text", "dropdown"],
  ["Date Added", "date", "input"],
  ["Date Modified", "date", "input"],
];

export const nextOfKinLabels = [
  ["Name", "text", "input"],
  ["Relation", "text", "input"],
  ["Email", "email", "input"],
  ["Address", "text", "input"],
  ["Phone Number", "tel", "input"],
  ["Emergency Contact", "tel", "input"],
  ["Created By", "text", "dropdown"],
  ["Updated By", "text", "dropdown"],
  ["Date Added", "date", "input"],
  ["Date Modified", "date", "input"],
];

export const previousGovernmentServiceLabels = [
  ["Institution", "text", "input"],
  ["Position", "text", "input"],
  ["Duration", "text", "input"],
  ["Created By", "text", "dropdown"],
  ["Updated By", "text", "dropdown"],
  ["Date Added", "date", "input"],
  ["Date Modified", "date", "input"],
];

export const serviceWithForcesLabels = [
  ["Service Date", "date", "input"],
  ["Last Unit", "text", "dropdown"],
  ["Service Number", "text", "input"],
  ["Military Rank", "text", "dropdown"],
  ["Created By", "text", "dropdown"],
  ["Updated By", "text", "dropdown"],
  ["Date Added", "date", "input"],
  ["Date Modified", "date", "input"],
];

export const terminationOfAppointmentLabels = [
  ["Cause", "text", "dropdown"],
  ["Authority", "text", "input"],
  ["Date", "date", "input"],
  ["Status", "text", "dropdown"],
  ["Created By", "text", "dropdown"],
  ["Updated By", "text", "dropdown"],
  ["Date Added", "date", "input"],
  ["Date Modified", "date", "input"],
];

export const modelLabels = {
  Employee: "employee",
  Occurrence: "occurrence",
  Children: "children",
  Course: "course",
  Identity: "identity",
  Spouse: "spouse",
  "Emergency | Next of Kin": "emergencyOrNextOfKin",
  "Previous Government Service": "previousGovernmentService",
  "Service With Forces": "serviceWithForces",
  "Termination of Appointment": "terminationOfAppointment",
};

export const inputRecordData = {
  Employee: employeeLabels,
  Occurrence: occurrenceLabels,
  Children: childrenLabels,
  Course: courseLabels,
  Identity: identityLabels,
  Spouse: spouseLabels,
  "Emergency | Next of Kin": nextOfKinLabels,
  "Previous Government Service": previousGovernmentServiceLabels,
  "Service With Forces": serviceWithForcesLabels,
  "Termination of Appointment": terminationOfAppointmentLabels,
};

export const allLabelKeys = {
  "Service ID": "serviceId",
  "Last Name": "lastName",
  "Other Names": "otherNames",
  "SSNIT Number": "socialSecurity",
  Category: "category",
  "Appointment Date": "appointmentDate",
  "Confirmation Date": "confirmationDate",
  Probation: "probation",
  "Entry Qualification": "entryQualification",
  Unit: "unit",
  Grade: "grade",
  Station: "station",
  "Date of Birth": "dob",
  Age: "age",
  Gender: "gender",
  Hometown: "hometown",
  Region: "region",
  Nationality: "nationality",
  Address: "address",
  Email: "email",
  "Marital Status": "maritalStatus",
  Religion: "religion",
  Structure: "structure",
  "Blood Group": "bloodGroup",
  Disable: "disable",
  Absence: "absence",
  "Start Date": "startDate",
  "End Date": "endDate",
  Authority: "authority",
  "Child Name": "childName",
  "Other Parent": "otherParent",
  "Course Type": "courseType",
  Place: "place",
  From: "dateCommenced",
  To: "dateEnded",
  Result: "result",
  Qualification: "qualification",
  "Voters ID": "votersId",
  "National ID": "nationalId",
  "GLICO ID": "glicoId",
  nhisId: "nhisId",
  "TIN Number": "tinNumber",
  Name: "name",
  Relation: "relation",
  "Phone Number": "phoneNumber",
  "Emergency Contact": "emergencyContact",
  LevelStep: "levelStep",
  "Monthly Salary": "monthlySalary",
  "Annual Salary": "annualSalary",
  Event: "event",
  Percentage: "percentageAdjustment",
  "WEF Date": "wefDate",
  Reason: "reason",
  Institution: "institution",
  Duration: "duration",
  Position: "position",
  "Military Rank": "militaryRank",
  "Service Date": "serviceDate",
  "Service Number": "serviceId",
  "Last Unit": "lastUnit",
  "Spouse Name": "spouseName",
  "Registration Number": "registrationNumber",
  "Marriage Date": "marriageDate",
  "Marriage Place": "marriagePlace",
  Status: "status",
  Cause: "cause",
  Date: "date",
  "Created By": "createdBy",
  "Updated By": "updatedBy",
  "Date Added": "dateAdded",
  "Date Modified": "dateModified",
};

export const rangeLabelKey = {
  "Equal to": "equalTo",
  "Less than": "lessThan",
  "Greater than": "greaterThan",
  Between: "between",
};

export const dropdownDataAPIEndpoints = {
  Employee: "api/employees/staff/options/",
  Occurrence: "api/occurrence/data/options/",
  Children: "api/children/dropdown-data/",
  Course: "api/courses/dropdown-data/",
  Identity: "api/identity/dropdown-data/",
  Spouse: "api/marriage/dropdown-data/",
  "Emergency | Next of Kin": "api/next-of-kin/dropdown-data/",
  "Previous Government Service":
    "api/previous-government-service/dropdown-data/",
  "Service With Forces": "api/service-with-forces/list-ranks-and-units/",
  "Termination of Appointment":
    "api/termination-of-appointment/list-causes-and-statuses/",
};

export const dropdownConfig = {
  "Created By": {
    dataKey: "users",
    labelKey: "fullname",
    valueKey: "id",
  },
  "Updated By": {
    dataKey: "users",
    labelKey: "fullname",
    valueKey: "id",
  },
  Unit: {
    dataKey: "units",
    labelKey: "unit_name",
    valueKey: "id",
  },
  Grade: {
    dataKey: "grades",
    labelKey: "grade_name",
    valueKey: "id",
  },
  Gender: {
    dataKey: "gender",
    labelKey: "sex",
    valueKey: "id",
  },
  Region: {
    dataKey: "region",
    labelKey: "region_name",
    valueKey: "id",
  },
  Religion: {
    dataKey: "religion",
    labelKey: "religion_name",
    valueKey: "id",
  },
  "Marital Status": {
    dataKey: "marital_status",
    labelKey: "marital_status_name",
    valueKey: "id",
  },
  Structure: {
    dataKey: "structure",
    labelKey: "structure_name",
    valueKey: "id",
  },
  "Blood Group": {
    dataKey: "blood_group",
    labelKey: "blood_group_name",
    valueKey: "id",
  },
  LevelStep: {
    dataKey: "level_step",
    labelKey: "level_step",
    valueKey: "id",
  },
  Event: {
    dataKey: "event",
    labelKey: "event_name",
    valueKey: "id",
  },
  Percentage: {
    dataKey: "salary_adjustment_percentage",
    labelKey: "percentage_adjustment",
    valueKey: "id",
  },
  "Last Unit": {
    dataKey: "units",
    labelKey: "unit_name",
    valueKey: "id",
  },
  "Military Rank": {
    dataKey: "military_ranks",
    labelKey: "rank",
    valueKey: "id",
  },
  Cause: {
    dataKey: "causes",
    labelKey: "termination_cause",
    valueKey: "id",
  },
  Status: {
    dataKey: "statuses",
    labelKey: "termination_status",
    valueKey: "id",
  },
};
