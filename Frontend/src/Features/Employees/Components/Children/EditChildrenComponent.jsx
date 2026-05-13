import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import ChildrenInputBoxes from "./ChildrenInputBoxesComponent";
import api from "../../../../api";
import { useState, useEffect } from "react";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { MdDelete } from "react-icons/md";
import askToDelete from "../../../../utils/askToDelete";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import ClipLoader from "react-spinners/ClipLoader";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";

export default function EditChildren() {
  const [initialData, setInitialData] = useState({});
  const [formData, setFormData] = useState({});
  const [loadingData, setLoadingData] = useState(true);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { setResponse } = useOutletContext();
  const { serviceId, childId } = useParams();

  const { theme } = useTheme();

  useEffect(() => {
    setFormData(initialData);
  }, [initialData]);

  useEffect(() => {
    const fetchChild = async () => {
      try {
        const res = await api.get(`api/children/${childId}/detail/`);
        setInitialData({
          childName: res.data.child_name,
          authority: res.data.authority,
          gender: {
            value: res.data.gender,
            label: res.data.gender_display,
          },
          otherParent: res.data.other_parent,
          dob: res.data.dob,
          createdAt: res.data.date_added,
          createdBy: res.data.created_by_display,
          updatedAt: res.data.date_modified,
          updatedBy: res.data.updated_by_display,
        });
        setLoadingData(false);
      } catch (error) {
        if (error.response?.status === 404) {
          setResponse({
            message: "Child record not found",
            type: "error",
            id: Date.now(),
          });
          navigate(`/home/employees/${serviceId}/children`);
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
    fetchChild();
  }, []);

  const updateChild = async () => {
    setLoading(true);

    const payload = {
      child_name: formData.childName,
      authority: formData.authority,
      gender: formData.gender.value,
      other_parent: formData.otherParent,
      dob: formData.dob,
    };

    try {
      const res = await api.patch(`api/children/${childId}/edit/`, payload);
      setFormData({
        childName: res.data.child_name,
        authority: res.data.authority,
        gender: {
          value: res.data.gender,
          label: res.data.gender_display,
        },
        otherParent: res.data.other_parent,
        dob: res.data.dob,
        createdAt: res.data.date_added,
        createdBy: res.data.created_by_display,
        updatedAt: res.data.date_modified,
        updatedBy: res.data.updated_by_display,
      });
      setResponse({
        message: "Child record updated",
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
      const res = await api.delete(`api/children/${childId}/delete/`);
      if (res.status === 204) {
        navigate(`/home/employees/${serviceId}/children`);
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
              onClick={() => navigate(`/home/employees/${serviceId}/children`)}
            >
              All Child Records
            </button>
          )}
        </div>
      </div>
      <div className={style.inputAndButtonsSection}>
        <ChildrenInputBoxes
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
              <button onClick={updateChild}>
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
