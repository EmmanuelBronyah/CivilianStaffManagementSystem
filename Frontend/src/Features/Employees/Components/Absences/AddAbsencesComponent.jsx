import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";
import { useState } from "react";
import AbsencesInputBoxes from "./AbsencesInputBoxesComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import ClipLoader from "react-spinners/ClipLoader";
import useFetchUserRole from "../../../hooks/fetchUserRoleHook";
import { useEffect } from "react";

export default function AddAbsences() {
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const { theme } = useTheme();
  const navigate = useNavigate();
  const { serviceId } = useParams();
  const { setResponse } = useOutletContext();
  const { role, response } = useFetchUserRole();

  useEffect(() => {
    if (!response) return;
    setResponse(response);
  });

  const addAbsences = async () => {
    setLoading(true);

    const payload = {
      employee: serviceId,
      absence: formData.absence,
      start_date: formData.startDate || null,
      end_date: formData.endDate || null,
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
            <button
              className={!role || role === "VIEWER" ? style.displayNone : ""}
              onClick={addAbsences}
            >
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
              className={`${style.cancelButton} ${!role || role === "VIEWER" ? style.displayNone : ""}`}
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
