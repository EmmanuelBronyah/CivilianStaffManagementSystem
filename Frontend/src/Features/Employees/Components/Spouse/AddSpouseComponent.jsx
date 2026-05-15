import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";
import { useState } from "react";
import SpouseInputBoxes from "./SpouseInputBoxesComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import ClipLoader from "react-spinners/ClipLoader";

export default function AddSpouse() {
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const { theme } = useTheme();
  const navigate = useNavigate();
  const { serviceId } = useParams();
  const { setResponse } = useOutletContext();

  const addSpouse = async () => {
    setLoading(true);

    const payload = {
      employee: serviceId,
      spouse_name: formData.spouseName,
      phone_number: formData.phoneNumber,
      address: formData.address,
      registration_number: formData.registrationNumber,
      marriage_date: formData.marriageDate || null,
      marriage_place: formData.marriagePlace,
    };

    try {
      const res = await api.post("api/marriage/create/", payload);
      setFormData({
        spouseName: res.data.spouse_name,
        phoneNumber: res.data.phone_number,
        address: res.data.address,
        registrationNumber: res.data.registration_number,
        marriageDate: res.data.marriage_date || null,
        marriagePlace: res.data.marriage_place,
      });
      setResponse({
        message: "Spouse saved",
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
            onClick={() => navigate(`/home/employees/${serviceId}/spouse`)}
          >
            All Spouses
          </button>
        </div>
      </div>
      <div className={style.inputAndButtonsSection}>
        <SpouseInputBoxes
          formData={formData}
          setFormData={setFormData}
          setResponse={setResponse}
        />
        <div className={style.addOccurrenceButtons}>
          <div className={style.addCancelButtons}>
            <button onClick={addSpouse}>
              {loading ? (
                <ClipLoader
                  size={13}
                  color={`${!theme ? "#1e1e1e" : "#d7fdd7"}`}
                />
              ) : (
                "Save Spouse"
              )}
            </button>
            <button
              className={style.cancelButton}
              onClick={() => navigate(`/home/employees/${serviceId}/spouse`)}
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
