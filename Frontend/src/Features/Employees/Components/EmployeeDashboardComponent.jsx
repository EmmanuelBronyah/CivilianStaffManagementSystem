import style from "../../../styles/components/employees.module.css";
import { useState, useEffect } from "react";
import { useTheme } from "../../../context/ThemeContext";
import api from "../../../api";
import getResponseMessages from "../../../utils/extractResponseMessage";
import Notification from "../../../Components/Common/NotificationComponent";
import EmployeePrimary from "./EmployeePrimaryComponent";
import { MdArrowBack, MdKeyboardArrowDown } from "react-icons/md";

export default function EmployeeDashboard({ serviceId, setEmployeePage }) {
  const [headerData, setHeaderData] = useState({
    serviceId: "",
    lastName: "",
    otherNames: "",
    age: "",
  });
  const [employeePrimaryData, setEmployeePrimaryData] = useState({});
  const [employeeSections, setEmployeeSections] = useState("Primary");

  const [visible, setVisible] = useState(false);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(true);

  const { theme } = useTheme();

  useEffect(() => {
    if (!response) return;

    setVisible(true);

    const timer = setTimeout(() => {
      setVisible(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, [response]);

  useEffect(() => {
    const fetchEmployee = async () => {
      try {
        const res = await api.get(`api/employees/staff/${serviceId}/detail/`);
        setHeaderData({
          serviceId: res.data.service_id,
          lastName: res.data.last_name,
          otherNames: res.data.other_names,
          age: res.data.age,
        });
        setEmployeePrimaryData({
          address: res.data.address,
          appointmentDate: res.data.appointment_date,
          confirmationDate: res.data.confirmation_date,
          bloodGroup: res.data.blood_group_display,
          category: res.data.category,
          disable: res.data.disable,
          dob: res.data.dob,
          email: res.data.email,
          entryQualification: res.data.entry_qualification,
          gender: res.data.gender_display,
          grade: res.data.grade_display,
          hometown: res.data.hometown,
          maritalStatus: res.data.marital_status_display,
          nationality: res.data.nationality,
          probation: res.data.probation,
          region: res.data.region_display,
          religion: res.data.religion_display,
          socialSecurity: res.data.social_security,
          station: res.data.station,
          structure: res.data.structure_display,
          unit: res.data.unit_display,
          createdBy: res.data.created_by_display,
          updatedBy: res.data.updated_by_display,
        });
      } catch (error) {
        setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
        return;
      }
    };
    fetchEmployee();
  }, []);

  return (
    <>
      <div className={`${style.employeeDashboard} ${!theme ? style.dark : ""}`}>
        <div className={`${style.employeeHeader} ${!theme ? style.dark : ""}`}>
          <div className={style.backIconAndServiceId}>
            <MdArrowBack
              className={style.icon}
              onClick={() => setEmployeePage("Sample Employees")}
            />
            <div className={style.serviceId}>{headerData.serviceId}</div>
          </div>

          <div className={style.nameAndAge}>
            <div
              className={style.name}
            >{`${headerData.lastName} ${headerData.otherNames}`}</div>
            <div className={style.age}>42 years</div>
          </div>
          <div className={style.employeeSections}>
            <p>Sections</p>
            <MdKeyboardArrowDown className={style.icon} />
            <div className={style.sectionsDropdown}>
              <ul>
                <li>Primary</li>
                <li>Occurrence</li>
                <li>Children</li>
                <li>Courses</li>
                <li>Absences</li>
                <li>Emergency | Next of Kin</li>
                <li>Spouse</li>
                <li>Termination of Appointment</li>
                <li>Identity</li>
                <li>Service With Forces</li>
                <li>Previous Government Services</li>
              </ul>
            </div>
          </div>
        </div>
        {employeeSections === "Primary" && (
          <EmployeePrimary data={employeePrimaryData} />
        )}
      </div>
      <Notification isVisible={visible} response={response} />
    </>
  );
}
