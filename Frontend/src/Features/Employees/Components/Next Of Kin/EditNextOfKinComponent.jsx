import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import NextOfKinInputBoxes from "./NextOfKinInputBoxesComponent";
import api from "../../../../api";
import { useState, useEffect } from "react";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { MdDelete } from "react-icons/md";
import askToDelete from "../../../../utils/askToDelete";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import ClipLoader from "react-spinners/ClipLoader";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";

export default function EditNextOfKin() {
  const [initialData, setInitialData] = useState({});
  const [formData, setFormData] = useState({});
  const [loadingData, setLoadingData] = useState(true);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { setResponse } = useOutletContext();
  const { serviceId, nextOfKinId } = useParams();

  const { theme } = useTheme();

  useEffect(() => {
    setFormData(initialData);
  }, [initialData]);

  useEffect(() => {
    const fetchNextOfKin = async () => {
      try {
        const res = await api.get(`api/next-of-kin/${nextOfKinId}/detail/`);
        setInitialData({
          name: res.data.name,
          relation: res.data.relation,
          email: res.data.next_of_kin_email,
          address: res.data.address,
          phoneNumber: res.data.phone_number,
          emergencyContact: res.data.emergency_contact,
          createdAt: res.data.date_added,
          createdBy: res.data.created_by_display,
          updatedAt: res.data.date_modified,
          updatedBy: res.data.updated_by_display,
        });
        setLoadingData(false);
      } catch (error) {
        if (error.response?.status === 404) {
          setResponse({
            message: "Next Of Kin record not found",
            type: "error",
            id: Date.now(),
          });
          navigate(`/home/employees/${serviceId}/nextOfKin`);
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
    fetchNextOfKin();
  }, []);

  const updateNextOfKin = async () => {
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
      const res = await api.patch(
        `api/next-of-kin/${nextOfKinId}/edit/`,
        payload,
      );
      setFormData({
        name: res.data.name,
        relation: res.data.relation,
        email: res.data.next_of_kin_email,
        address: res.data.address,
        phoneNumber: res.data.phone_number,
        emergencyContact: res.data.emergency_contact,
        createdAt: res.data.date_added,
        createdBy: res.data.created_by_display,
        updatedAt: res.data.date_modified,
        updatedBy: res.data.updated_by_display,
      });
      setResponse({
        message: "Next Of Kin updated",
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
      const res = await api.delete(`api/next-of-kin/${nextOfKinId}/delete/`);
      if (res.status === 204) {
        navigate(`/home/employees/${serviceId}/nextOfKin`);
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
              onClick={() => navigate(`/home/employees/${serviceId}/nextOfKin`)}
            >
              All Next Of Kins
            </button>
          )}
        </div>
      </div>
      <div className={style.inputAndButtonsSection}>
        <NextOfKinInputBoxes
          formData={formData}
          setFormData={setFormData}
          loadingData={loadingData}
        />
        <div className={style.editOccurrenceButtons}>
          <div className={style.emptyDiv}></div>
          <div className={style.updateCancelButtons}>
            {loadingData ? (
              <BaseSkeleton width={120} height={38} />
            ) : (
              <button onClick={updateNextOfKin}>
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
