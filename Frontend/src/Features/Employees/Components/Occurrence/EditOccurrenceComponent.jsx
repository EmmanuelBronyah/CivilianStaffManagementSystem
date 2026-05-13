import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import OccurrenceInputBoxes from "./OccurrenceInputBoxesComponent";
import api from "../../../../api";
import { useState, useEffect } from "react";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { MdDelete } from "react-icons/md";
import askToDelete from "../../../../utils/askToDelete";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import ClipLoader from "react-spinners/ClipLoader";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";

export default function EditOccurrence() {
  const [initialData, setInitialData] = useState({});
  const [formData, setFormData] = useState({});
  const [loadingData, setLoadingData] = useState(true);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { setResponse } = useOutletContext();
  const { serviceId, occurrenceId } = useParams();

  const { theme } = useTheme();

  useEffect(() => {
    setFormData(initialData);
  }, [initialData]);

  useEffect(() => {
    const fetchOccurrence = async () => {
      try {
        const res = await api.get(`api/occurrence/${occurrenceId}/`);
        setInitialData({
          grade: {
            value: res.data.grade,
            label: res.data.grade_display,
          },
          authority: res.data.authority,
          levelStep: {
            value: res.data.level_step,
            label: res.data.level_step_display,
          },
          monthlySalary: res.data.monthly_salary,
          annualSalary: res.data.annual_salary,
          event: {
            value: res.data.event,
            label: res.data.event_display,
          },
          wefDate: res.data.wef_date,
          reason: res.data.reason,
          createdAt: res.data.date_added,
          createdBy: res.data.created_by_display,
          updatedAt: res.data.date_modified,
          updatedBy: res.data.updated_by_display,
        });
        setLoadingData(false);
      } catch (error) {
        if (error.response.status === 404) {
          setResponse({
            message: "Occurrence not found",
            type: "error",
            id: Date.now(),
          });
          navigate(`/home/employees/${serviceId}/occurrence`);
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
    fetchOccurrence();
  }, []);

  const updateOccurrence = async () => {
    setLoading(true);

    const payload = {
      grade: formData.grade.value,
      authority: formData.authority,
      level_step: formData.levelStep.value,
      monthly_salary: formData.monthlySalary,
      annual_salary: formData.annualSalary,
      event: formData.event.value,
      percentage_adjustment: formData?.percentageAdjustment?.label || null,
      wef_date: formData.wefDate,
      reason: formData.reason,
    };

    try {
      const res = await api.patch(
        `api/occurrence/${occurrenceId}/edit/`,
        payload,
      );
      setFormData({
        grade: {
          value: res.data.grade,
          label: res.data.grade_display,
        },
        authority: res.data.authority,
        levelStep: {
          value: res.data.level_step,
          label: res.data.level_step_display,
        },
        monthlySalary: res.data.monthly_salary,
        annualSalary: res.data.annual_salary,
        event: {
          value: res.data.event,
          label: res.data.event_display,
        },
        wefDate: res.data.wef_date,
        reason: res.data.reason,
        createdAt: res.data.date_added,
        createdBy: res.data.created_by_display,
        updatedAt: res.data.date_modified,
        updatedBy: res.data.updated_by_display,
      });
      setResponse({
        message: "Occurrence updated",
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
      const res = await api.delete(`api/occurrence/${occurrenceId}/delete/`);
      if (res.status === 204) {
        navigate(`/home/employees/${serviceId}/occurrence`);
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
                navigate(`/home/employees/${serviceId}/occurrence`)
              }
            >
              All Occurrences
            </button>
          )}
        </div>
      </div>
      <div className={style.inputAndButtonsSection}>
        <OccurrenceInputBoxes
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
              <button onClick={updateOccurrence}>
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
