import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";
import { useState } from "react";
import ServiceWithForcesInputBoxes from "./ServiceWithForcesInputBoxesComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import ClipLoader from "react-spinners/ClipLoader";

export default function AddService() {
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
      last_unit: formData.lastUnit?.value,
      service_id: formData.serviceId,
      military_rank: formData.militaryRank?.value,
      service_date: formData.serviceDate || null,
    };
    try {
      const res = await api.post("api/service-with-forces/create/", payload);
      setFormData({
        lastUnit: {
          value: res.data.last_unit,
          label: res.data.last_unit_display,
        },
        militaryRank: {
          value: res.data.military_rank,
          label: res.data.military_rank_display,
        },
        serviceId: res.data.service_id,
        serviceDate: res.data.service_date,
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
              navigate(`/home/employees/${serviceId}/serviceWithForces`)
            }
          >
            All Service Records
          </button>
        </div>
      </div>
      <div className={style.inputAndButtonsSection}>
        <ServiceWithForcesInputBoxes
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
                navigate(`/home/employees/${serviceId}/serviceWithForces`)
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
