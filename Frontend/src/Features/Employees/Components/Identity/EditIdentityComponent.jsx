import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import IdentityInputBoxes from "./IdentityInputBoxesComponent";
import api from "../../../../api";
import { useState, useEffect } from "react";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { MdDelete } from "react-icons/md";
import askToDelete from "../../../../utils/askToDelete";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import ClipLoader from "react-spinners/ClipLoader";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";

export default function EditIdentity() {
  const [initialData, setInitialData] = useState({});
  const [formData, setFormData] = useState({});
  const [loadingData, setLoadingData] = useState(true);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { setResponse } = useOutletContext();
  const { serviceId, identityId } = useParams();

  const { theme } = useTheme();

  useEffect(() => {
    setFormData(initialData);
  }, [initialData]);

  useEffect(() => {
    const fetchIdentity = async () => {
      try {
        const res = await api.get(`api/identity/${serviceId}/detail/`);
        setInitialData({
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
        setLoadingData(false);
      } catch (error) {
        if (error.response.status === 404) {
          setResponse({
            message: "Identity record not found",
            type: "error",
            id: Date.now(),
          });
          navigate(`/home/employees/${serviceId}/identity`);
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
    fetchIdentity();
  }, []);

  const updateIdentity = async () => {
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
      const res = await api.patch(`api/identity/${identityId}/edit/`, payload);
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
        message: "Identity record updated",
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
      const res = await api.delete(`api/identity/${identityId}/delete/`);
      if (res.status === 204) {
        navigate(`/home/employees/${serviceId}/identity`);
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
              onClick={() => navigate(`/home/employees/${serviceId}/identity`)}
            >
              All Identity Records
            </button>
          )}
        </div>
      </div>
      <div className={style.inputAndButtonsSection}>
        <IdentityInputBoxes
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
              <button onClick={updateIdentity}>
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
