import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";
import { useState } from "react";
import PreviousGovernmentServiceInputBoxes from "./PreviousGovernmentServiceInputBoxesComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import ClipLoader from "react-spinners/ClipLoader";

export default function AddPreviousGovernmentService() {
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const { theme } = useTheme();
  const navigate = useNavigate();
  const { serviceId } = useParams();
  const { setResponse } = useOutletContext();

  const addService = async () => {
    setLoading(true);

    const payload = {
      employee: serviceId,
      institution: formData.institution,
      duration: formData.duration,
      position: formData.position,
    };
    try {
      const res = await api.post(
        "api/previous-government-service/create/",
        payload,
      );
      setFormData({
        institution: res.data.institution,
        duration: res.data.duration,
        position: res.data.position,
      });
      setResponse({
        message: "Service saved",
        id: Date.now(),
      });
      setLoading(false);
    } catch (error) {
      setResponse({
        message: getResponseMessages(error.response),
        type: "error",
        id: Date.now(),
      });
      setLoading(false);
    }
  };

  return (
    <div
      className={`${style.editEmployeeOccurrence} ${!theme ? style.dark : ""}`}
    >
      <div className={style.occurrencePageButtonAndTableContainer}>
        <div className={style.addOccurrenceButtonContainer}>
          <button
            className={style.addOccurrence}
            onClick={() =>
              navigate(`/home/employees/${serviceId}/previousGovernmentService`)
            }
          >
            All Service Records
          </button>
        </div>
      </div>
      <div className={style.inputAndButtonsSection}>
        <PreviousGovernmentServiceInputBoxes
          formData={formData}
          setFormData={setFormData}
          setResponse={setResponse}
        />
        <div className={style.addOccurrenceButtons}>
          <div className={style.addCancelButtons}>
            <button onClick={addService}>
              {loading ? (
                <ClipLoader
                  size={13}
                  color={`${!theme ? "#1e1e1e" : "#d7fdd7"}`}
                />
              ) : (
                "Save Service"
              )}
            </button>
            <button
              className={style.cancelButton}
              onClick={() =>
                navigate(
                  `/home/employees/${serviceId}/previousGovernmentService`,
                )
              }
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
