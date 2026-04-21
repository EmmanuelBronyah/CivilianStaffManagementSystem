import style from "../../../styles/components/employees.module.css";
import { useState, useEffect } from "react";
import { useTheme } from "../../../context/ThemeContext";
import api from "../../../api";
import getResponseMessages from "../../../utils/extractResponseMessage";
import EmployeePrimary from "./EmployeePrimaryComponent";
import { MdArrowBack, MdKeyboardArrowDown } from "react-icons/md";

export default function EmployeeDashboard({
  serviceId,
  setEmployeePage,
  setResponse,
}) {
  const [headerData, setHeaderData] = useState({
    serviceId: "",
    lastName: "",
    otherNames: "",
    age: "",
  });
  const [employeeSections, setEmployeeSections] = useState("Primary");
  const [showDropdown, setShowDropdown] = useState(false);

  const [initialData, setInitialData] = useState({});
  const [formData, setFormData] = useState({});

  const [loading, setLoading] = useState(true);

  const { theme } = useTheme();

  useEffect(() => {
    setFormData(initialData);
  }, [initialData]);

  useEffect(() => {
    const fetchEmployee = async () => {
      try {
        const res = await api.get(`api/employees/staff/${serviceId}/detail/`);
        // console.log(res.data);

        setHeaderData({
          serviceId: res.data.service_id,
          lastName: res.data.last_name,
          otherNames: res.data.other_names,
          age: res.data.age,
        });
        setInitialData({
          serviceId: res.data.service_id,
          lastName: res.data.last_name,
          otherNames: res.data.other_names,
          address: res.data.address,
          appointmentDate: res.data.appointment_date,
          confirmationDate: res.data.confirmation_date,
          bloodGroup: {
            value: res.data.blood_group,
            label: res.data.blood_group_display,
          },
          category: res.data.category,
          disable: res.data.disable,
          dob: res.data.dob,
          email: res.data.email,
          entryQualification: res.data.entry_qualification,
          gender: {
            value: res.data.gender,
            label: res.data.gender_display,
          },
          grade: {
            value: res.data.grade,
            label: res.data.grade_display,
          },
          hometown: res.data.hometown,
          maritalStatus: {
            value: res.data.marital_status,
            label: res.data.marital_status_display,
          },
          nationality: res.data.nationality,
          probation: res.data.probation,
          region: {
            value: res.data.region,
            label: res.data.region_display,
          },
          religion: {
            value: res.data.religion,
            label: res.data.religion_display,
          },
          socialSecurity: res.data.social_security,
          station: res.data.station,
          structure: {
            value: res.data.structure,
            label: res.data.structure_display,
          },
          unit: {
            value: res.data.unit,
            label: res.data.unit_display,
          },
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
            <div className={style.age}>{headerData.age || "__"} years</div>
          </div>
          <div
            className={style.employeeSections}
            onClick={() => setShowDropdown((prev) => !prev)}
          >
            <p>Sections</p>
            <MdKeyboardArrowDown className={style.icon} />
            <div
              className={style.sectionsDropdown}
              data-show-dropdown={showDropdown}
            >
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
          <EmployeePrimary
            setHeaderData={setHeaderData}
            initialData={initialData}
            setInitialData={setInitialData}
            formData={formData}
            setFormData={setFormData}
            setResponse={setResponse}
          />
        )}
      </div>
    </>
  );
}
