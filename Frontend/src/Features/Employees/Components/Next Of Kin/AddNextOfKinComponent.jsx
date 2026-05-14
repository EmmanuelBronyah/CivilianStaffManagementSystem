import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";
import { useState } from "react";
import NextOfKinInputBoxes from "./NextOfKinInputBoxesComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import ClipLoader from "react-spinners/ClipLoader";

export default function AddNextOfKin() {
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const { theme } = useTheme();
  const navigate = useNavigate();
  const { serviceId } = useParams();
  const { setResponse } = useOutletContext();

  const addNextOfKin = async () => {
    setLoading(true);

    const payload = {
      employee: serviceId,
      name: formData.name,
      relation: formData.relation,
      next_of_kin_email: formData.email,
      address: formData.address,
      phone_number: formData.phoneNumber,
      emergency_contact: formData.emergencyContact,
    };

    try {
      const res = await api.post("api/next-of-kin/create/", payload);
      setFormData({
        name: res.data.name,
        relation: res.data.relation,
        email: res.data.next_of_kin_email,
        address: res.data.address,
        phoneNumber: res.data.phone_number,
        emergencyContact: res.data.emergency_contact,
      });
      setResponse({
        message: "Next Of Kin saved",
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
            onClick={() => navigate(`/home/employees/${serviceId}/nextOfKin`)}
          >
            All Next Of Kins
          </button>
        </div>
      </div>
      <div className={style.inputAndButtonsSection}>
        <NextOfKinInputBoxes
          formData={formData}
          setFormData={setFormData}
          setResponse={setResponse}
        />
        <div className={style.addOccurrenceButtons}>
          <div className={style.addCancelButtons}>
            <button onClick={addNextOfKin}>
              {loading ? (
                <ClipLoader
                  size={13}
                  color={`${!theme ? "#1e1e1e" : "#d7fdd7"}`}
                />
              ) : (
                "Save Next Of Kin"
              )}
            </button>
            <button
              className={style.cancelButton}
              onClick={() => navigate(`/home/employees/${serviceId}/nextOfKin`)}
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
