import style from "../../../../styles/components/userscomponent.module.css";
import AddEmployeeInputBoxes from "./AddEmployeeInputBoxes";
import { useTheme } from "../../../../context/ThemeContext";
import { useState, useEffect } from "react";
import Notification from "../../../../Components/Common/NotificationComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import ClipLoader from "react-spinners/ClipLoader";
import { Link } from "react-router-dom";
import useFetchUserRole from "../../../hooks/fetchUserRoleHook";
import { useOutletContext } from "react-router-dom";

export default function AddEmployee() {
  const initialFormData = {};
  const [formData, setFormData] = useState(initialFormData);
  const { setResponse } = useOutletContext();
  const [loading, setLoading] = useState(false);
  const [loadingData, setLoadingData] = useState(true);

  const { theme } = useTheme();
  const { role, errorResponse } = useFetchUserRole();

  useEffect(() => {
    if (!errorResponse) return;
    setResponse(errorResponse);
  });

  const registerEmployee = async () => {
    const payload = {
      service_id: formData.serviceId,
      last_name: formData.lastName,
      other_names: formData.otherNames,
      social_security: formData.ssnitNumber,
      unit: formData.unit.value,
      grade: formData.grade.value,
      gender: formData.gender.value,
      appointment_date: formData.appointmentDate,
    };
    try {
      const res = await api.post("api/employees/staff/create/", payload);
      console.log("Response -> ", res.data);

      setFormData({
        serviceId: res.data.service_id,
        lastName: res.data.last_name,
        otherNames: res.data.other_names,
        dob: res.data.dob,
        ssnitNumber: res.data.social_security,
        gender: { label: res.data.gender_display, value: res.data.gender },
        appointmentDate: res.data.appointment_date,
        grade: { label: res.data.grade_display, value: res.data.grade },
        unit: { label: res.data.unit_display, value: res.data.unit },
      });
      setResponse({
        message: "Employee saved",
        id: Date.now(),
      });
    } catch (error) {
      setResponse({
        message: getResponseMessages(error.response),
        type: "error",
        id: Date.now(),
      });
    }
  };

  return (
    <>
      <div
        className={`${style.addUserComponentContainer} ${!theme ? style.dark : ""}`}
      >
        <div className={style.allUsersButtonContainer}>
          <Link to="/home/employees">
            <button>Sample Employees</button>
          </Link>
        </div>
        <div className={style.addUserContainer}>
          <div className={style.addUserTitle}>
            <p>Add A New Employee</p>
          </div>
          <AddEmployeeInputBoxes
            formData={formData}
            setFormData={setFormData}
            setResponse={setResponse}
            loading={loadingData}
            setLoading={setLoadingData}
          />
          <div className={style.buttonsContainer}>
            <div className={style.addUserButton}>
              <button
                className={!role || role === "VIEWER" ? style.displayNone : ""}
                disabled={loading}
                onClick={registerEmployee}
              >
                {loading ? (
                  <ClipLoader
                    size={13}
                    color={`${!theme ? "#1e1e1e" : "#d7fdd7"}`}
                  />
                ) : (
                  "Save"
                )}
              </button>
            </div>

            <div
              className={`${style.discardButton} ${!role || role === "VIEWER" ? style.displayNone : ""}`}
            >
              <button disabled={loading} /*onClick={clearData}*/>
                Discard
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
