import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";
import { useState } from "react";
import AbsencesInputBoxes from "./AbsencesInputBoxesComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import ClipLoader from "react-spinners/ClipLoader";

export default function AddAbsences() {
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const { theme } = useTheme();
  const navigate = useNavigate();
  const { serviceId } = useParams();
  const { setResponse } = useOutletContext();

  const addAbsences = async () => {
    setLoading(true);

    const payload = {
      employee: serviceId,
      absence: formData.absence,
      start_date: formData.startDate,
      end_date: formData.endDate,
      authority: formData.authority,
    };

    try {
      const res = await api.post("api/absences/create/", payload);
      setFormData({
        absence: res.data.absence,
        startDate: res.data.start_date,
        endDate: res.data.end_date,
        authority: res.data.authority,
      });
      setResponse({
        message: "Absences saved",
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
            onClick={() => navigate(`/home/employees/${serviceId}/absences`)}
          >
            All Absences
          </button>
        </div>
      </div>
      <div className={style.inputAndButtonsSection}>
        <AbsencesInputBoxes
          formData={formData}
          setFormData={setFormData}
          setResponse={setResponse}
        />
        <div className={style.addOccurrenceButtons}>
          <div className={style.addCancelButtons}>
            <button onClick={addAbsences}>
              {loading ? (
                <ClipLoader
                  size={13}
                  color={`${!theme ? "#1e1e1e" : "#d7fdd7"}`}
                />
              ) : (
                "Save Absences"
              )}
            </button>
            <button
              className={style.cancelButton}
              onClick={() => navigate(`/home/employees/${serviceId}/absences`)}
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
