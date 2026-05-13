import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";
import { useState } from "react";
import ChildrenInputBoxes from "./ChildrenInputBoxesComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import ClipLoader from "react-spinners/ClipLoader";

export default function AddChildren() {
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const { theme } = useTheme();
  const navigate = useNavigate();
  const { serviceId } = useParams();
  const { setResponse } = useOutletContext();

  const addChild = async () => {
    setLoading(true);

    const payload = {
      employee: serviceId,
      child_name: formData.childName,
      authority: formData.authority,
      gender: formData.gender.value,
      other_parent: formData.otherParent,
      dob: formData.dob,
    };

    try {
      const res = await api.post("api/children/create/", payload);
      setFormData({
        childName: res.data.child_name,
        authority: res.data.authority,
        gender: {
          value: res.data.gender,
          label: res.data.gender_display,
        },
        otherParent: res.data.other_parent,
        dob: res.data.dob,
      });
      setResponse({
        message: "Child record saved",
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
            onClick={() => navigate(`/home/employees/${serviceId}/children`)}
          >
            All Children Records
          </button>
        </div>
      </div>
      <div className={style.inputAndButtonsSection}>
        <ChildrenInputBoxes
          formData={formData}
          setFormData={setFormData}
          setResponse={setResponse}
        />
        <div className={style.addOccurrenceButtons}>
          <div className={style.addCancelButtons}>
            <button onClick={addChild}>
              {loading ? (
                <ClipLoader
                  size={13}
                  color={`${!theme ? "#1e1e1e" : "#d7fdd7"}`}
                />
              ) : (
                "Save Child Record"
              )}
            </button>
            <button
              className={style.cancelButton}
              onClick={() => navigate(`/home/employees/${serviceId}/children`)}
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
