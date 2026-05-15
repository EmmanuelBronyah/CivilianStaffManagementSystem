import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";
import { useState } from "react";
import TerminationInputBoxes from "./TerminationInputBoxesComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import ClipLoader from "react-spinners/ClipLoader";

export default function AddTermination() {
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const { theme } = useTheme();
  const navigate = useNavigate();
  const { serviceId } = useParams();
  const { setResponse } = useOutletContext();

  const addTermination = async () => {
    setLoading(true);

    const payload = {
      employee: serviceId,
      cause: formData.cause?.value,
      status: formData.status?.value,
      authority: formData.authority,
      date: formData.date || null,
    };
    try {
      const res = await api.post(
        "api/termination-of-appointment/create/",
        payload,
      );
      setFormData({
        cause: {
          value: res.data.cause,
          label: res.data.cause_display,
        },
        status: {
          value: res.data.status,
          label: res.data.status_display,
        },
        authority: res.data.authority,
        date: res.data.date,
      });
      setResponse({
        message: "Termination record saved",
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
            onClick={() => navigate(`/home/employees/${serviceId}/termination`)}
          >
            All Termination Records
          </button>
        </div>
      </div>
      <div className={style.inputAndButtonsSection}>
        <TerminationInputBoxes
          formData={formData}
          setFormData={setFormData}
          setResponse={setResponse}
        />
        <div className={style.addOccurrenceButtons}>
          <div className={style.addCancelButtons}>
            <button onClick={addTermination}>
              {loading ? (
                <ClipLoader
                  size={13}
                  color={`${!theme ? "#1e1e1e" : "#d7fdd7"}`}
                />
              ) : (
                "Save Termination Record"
              )}
            </button>
            <button
              className={style.cancelButton}
              onClick={() =>
                navigate(`/home/employees/${serviceId}/termination`)
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
