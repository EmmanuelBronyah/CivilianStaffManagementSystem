import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import ServiceWithForcesInputBoxes from "./ServiceWithForcesInputBoxesComponent";
import api from "../../../../api";
import { useState, useEffect } from "react";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { MdDelete } from "react-icons/md";
import askToDelete from "../../../../utils/askToDelete";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import ClipLoader from "react-spinners/ClipLoader";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";

export default function EditService() {
  const [initialData, setInitialData] = useState({});
  const [formData, setFormData] = useState({});
  const [loadingData, setLoadingData] = useState(true);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { setResponse } = useOutletContext();
  const { serviceId, serviceWithForcesId } = useParams();

  const { theme } = useTheme();

  useEffect(() => {
    setFormData(initialData);
  }, [initialData]);

  useEffect(() => {
    const fetchService = async () => {
      try {
        const res = await api.get(
          `api/service-with-forces/${serviceWithForcesId}/detail/`,
        );
        setInitialData({
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
          createdAt: res.data.date_added,
          createdBy: res.data.created_by_display,
          updatedAt: res.data.date_modified,
          updatedBy: res.data.updated_by_display,
        });
        setLoadingData(false);
      } catch (error) {
        if (error.response.status === 404) {
          setResponse({
            message: "Service record not found",
            type: "error",
            id: Date.now(),
          });
          navigate(`/home/employees/${serviceId}/serviceWithForces`);
          return;
        }

        setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
        return;
      }
    };
    fetchService();
  }, []);

  const updateService = async () => {
    setLoading(true);

    const payload = {
      employee: serviceId,
      last_unit: formData.lastUnit?.value,
      service_id: formData.serviceId,
      military_rank: formData.militaryRank?.value,
      service_date: formData.serviceDate || null,
    };

    try {
      const res = await api.patch(
        `api/service-with-forces/${serviceWithForcesId}/edit/`,
        payload,
      );
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
        createdAt: res.data.date_added,
        createdBy: res.data.created_by_display,
        updatedAt: res.data.date_modified,
        updatedBy: res.data.updated_by_display,
      });
      setResponse({
        message: "Service updated",
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
      return;
    }
  };

  const discardChanges = () => {
    const updatedInitialData = {
      ...initialData,
      createdAt: formData.createdAt,
      createdBy: formData.createdBy,
      updatedAt: formData.updatedAt,
      updatedBy: formData.updatedBy,
    };

    setFormData(updatedInitialData);
  };

  const initiateDeletion = async () => {
    const result = await askToDelete(theme);
    if (!result.isConfirmed) return;

    try {
      const res = await api.delete(
        `api/service-with-forces/${serviceWithForcesId}/delete/`,
      );
      if (res.status === 204) {
        navigate(`/home/employees/${serviceId}/serviceWithForces`);
      }
    } catch (error) {
      setResponse({
        message: getResponseMessages(error.response),
        type: "error",
        id: Date.now(),
      });
      return;
    }
  };

  return (
    <div
      className={`${style.editEmployeeOccurrence} ${!theme ? style.dark : ""}`}
    >
      <div className={style.occurrencePageButtonAndTableContainer}>
        <div className={style.addOccurrenceButtonContainer}>
          {loadingData ? (
            <BaseSkeleton width={170} height={39} />
          ) : (
            <button
              className={style.addOccurrence}
              onClick={() =>
                navigate(`/home/employees/${serviceId}/serviceWithForces`)
              }
            >
              All Service Records
            </button>
          )}
        </div>
      </div>
      <div className={style.inputAndButtonsSection}>
        <ServiceWithForcesInputBoxes
          formData={formData}
          setFormData={setFormData}
          setResponse={setResponse}
          loadingData={loadingData}
          setLoadingData={setLoadingData}
        />
        <div className={style.editOccurrenceButtons}>
          <div className={style.emptyDiv}></div>
          <div className={style.updateCancelButtons}>
            {loadingData ? (
              <BaseSkeleton width={120} height={38} />
            ) : (
              <button onClick={updateService}>
                {loading ? (
                  <ClipLoader
                    size={13}
                    color={`${!theme ? "#1e1e1e" : "#d7fdd7"}`}
                  />
                ) : (
                  "Save Changes"
                )}
              </button>
            )}
            {loadingData ? (
              <BaseSkeleton width={120} height={38} />
            ) : (
              <button className={style.cancelButton} onClick={discardChanges}>
                Cancel
              </button>
            )}
          </div>
          {loadingData ? (
            <BaseSkeleton width={40} />
          ) : (
            <MdDelete className={style.trashIcon} onClick={initiateDeletion} />
          )}
        </div>
      </div>
    </div>
  );
}
