import style from "../../../../styles/components/employees.module.css";
import { useState, useEffect } from "react";
import { useTheme } from "../../../../context/ThemeContext";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { MdArrowBack, MdKeyboardArrowDown } from "react-icons/md";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import EmployeeOccurrence from "../Occurrence/EmployeeOccurrenceComponent";
import { useParams } from "react-router-dom";
import { Outlet, useOutletContext, useNavigate } from "react-router-dom";

export default function EmployeeDashboard() {
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
  const { serviceId } = useParams();
  const { setResponse } = useOutletContext();
  const navigate = useNavigate();

  const { theme } = useTheme();

  useEffect(() => {
    setFormData(initialData);
  }, [initialData]);

  useEffect(() => {
    const fetchEmployee = async () => {
      try {
        const res = await api.get(`api/employees/staff/${serviceId}/detail/`);
        setLoading(false);
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
          age: res.data.age,
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
          createdAt: res.data.created_at,
          updatedAt: res.data.updated_at,
          createdBy: res.data.created_by_display,
          updatedBy: res.data.updated_by_display,
        });
      } catch (error) {
        setLoading(false);
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
              className={style.backIcon}
              onClick={() => navigate(`/home/employees`)}
            />
            {loading ? (
              <BaseSkeleton width={100} height={34} />
            ) : (
              <div className={style.serviceId}>{headerData.serviceId}</div>
            )}
          </div>

          <div className={style.nameAndAge}>
            {loading ? (
              <BaseSkeleton width={200} height={42} />
            ) : (
              <div
                className={style.name}
              >{`${headerData.lastName} ${headerData.otherNames}`}</div>
            )}
            {loading ? (
              <BaseSkeleton width={60} height={33} />
            ) : (
              <div className={style.age}>{headerData.age || "__"} years</div>
            )}
          </div>
          {loading ? (
            <BaseSkeleton width={100} height={33} />
          ) : (
            <div
              className={style.employeeSections}
              onClick={() => setShowDropdown((prev) => !prev)}
            >
              <p>{employeeSections}</p>
              <MdKeyboardArrowDown className={style.arrowDownIcon} />
              <div
                className={style.sectionsDropdown}
                data-show-dropdown={showDropdown}
              >
                <ul>
                  <li
                    onClick={() => {
                      setEmployeeSections("Primary");
                      navigate(`/home/employees/${serviceId}`);
                    }}
                  >
                    Primary
                  </li>
                  <li
                    onClick={() => {
                      setEmployeeSections("Occurrence");
                      navigate(`/home/employees/${serviceId}/occurrence`);
                    }}
                  >
                    Occurrence
                  </li>
                  <li
                    onClick={() => {
                      setEmployeeSections("Children");
                      navigate(`/home/employees/${serviceId}/children`);
                    }}
                  >
                    Children
                  </li>
                  <li
                    onClick={() => {
                      setEmployeeSections("Courses");
                      navigate(`/home/employees/${serviceId}/courses`);
                    }}
                  >
                    Courses
                  </li>
                  <li
                    onClick={() => {
                      setEmployeeSections("Absences");
                      navigate(`/home/employees/${serviceId}/absences`);
                    }}
                  >
                    Absences
                  </li>
                  <li
                    onClick={() => {
                      setEmployeeSections("Emergency | Next of Kin");
                      navigate(`/home/employees/${serviceId}/nextOfKin`);
                    }}
                  >
                    Emergency | Next of Kin
                  </li>
                  <li
                    onClick={() => {
                      setEmployeeSections("Spouse");
                      navigate(`/home/employees/${serviceId}/spouse`);
                    }}
                  >
                    Spouse
                  </li>
                  <li
                    onClick={() => {
                      setEmployeeSections("Termination of Appointment");
                      navigate(`/home/employees/${serviceId}/termination`);
                    }}
                  >
                    Termination of Appointment
                  </li>
                  <li
                    onClick={() => {
                      setEmployeeSections("Identity");
                      navigate(`/home/employees/${serviceId}/identity`);
                    }}
                  >
                    Identity
                  </li>
                  <li
                    onClick={() => {
                      setEmployeeSections("Service With Forces");
                      navigate(
                        `/home/employees/${serviceId}/serviceWithForces`,
                      );
                    }}
                  >
                    Service With Forces
                  </li>
                  <li
                    onClick={() => {
                      setEmployeeSections("Previous Government Services");
                      navigate(
                        `/home/employees/${serviceId}/previousGovernmentServices`,
                      );
                    }}
                  >
                    Previous Government Services
                  </li>
                </ul>
              </div>
            </div>
          )}
        </div>
        <Outlet
          context={{
            setHeaderData,
            initialData,
            setInitialData,
            formData,
            setFormData,
            setResponse,
          }}
        />
      </div>
    </>
  );
}
