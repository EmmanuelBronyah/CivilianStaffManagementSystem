import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";
import { useState } from "react";
import IdentityInputBoxes from "./IdentityInputBoxesComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import ClipLoader from "react-spinners/ClipLoader";

export default function AddIdentity() {
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const { theme } = useTheme();
  const navigate = useNavigate();
  const { serviceId } = useParams();
  const { setResponse } = useOutletContext();

  const addIdentity = async () => {
    setLoading(true);

    const payload = {
      employee: serviceId,
      voters_id: formData.votersId,
      national_id: formData.nationalId,
      glico_id: formData.glicoId,
      nhis_id: formData.nhisId,
      tin_number: formData.tinNumber,
    };
    try {
      const res = await api.post("api/identity/create/", payload);
      setFormData({
        votersId: res.data.voters_id,
        nationalId: res.data.national_id,
        glicoId: res.data.glico_id,
        nhisId: res.data.nhis_id,
        tinNumber: res.data.tin_number,
        createdAt: res.data.date_added,
        createdBy: res.data.created_by_display,
        updatedAt: res.data.date_modified,
        updatedBy: res.data.updated_by_display,
      });
      setResponse({
        message: "Identity record saved",
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
            onClick={() => navigate(`/home/employees/${serviceId}/identity`)}
          >
            All Identity Records
          </button>
        </div>
      </div>
      <div className={style.inputAndButtonsSection}>
        <IdentityInputBoxes
          formData={formData}
          setFormData={setFormData}
          setResponse={setResponse}
        />
        <div className={style.addOccurrenceButtons}>
          <div className={style.addCancelButtons}>
            <button onClick={addIdentity}>
              {loading ? (
                <ClipLoader
                  size={13}
                  color={`${!theme ? "#1e1e1e" : "#d7fdd7"}`}
                />
              ) : (
                "Save Identity Record"
              )}
            </button>
            <button
              className={style.cancelButton}
              onClick={() => navigate(`/home/employees/${serviceId}/identity`)}
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
