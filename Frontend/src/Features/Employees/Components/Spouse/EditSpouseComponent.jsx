import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import SpouseInputBoxes from "./SpouseInputBoxesComponent";
import api from "../../../../api";
import { useState, useEffect } from "react";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { MdDelete } from "react-icons/md";
import askToDelete from "../../../../utils/askToDelete";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import ClipLoader from "react-spinners/ClipLoader";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";

export default function EditSpouse() {
  const [initialData, setInitialData] = useState({});
  const [formData, setFormData] = useState({});
  const [loadingData, setLoadingData] = useState(true);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { setResponse } = useOutletContext();
  const { serviceId, spouseId } = useParams();

  const { theme } = useTheme();

  useEffect(() => {
    setFormData(initialData);
  }, [initialData]);

  useEffect(() => {
    const fetchSpouse = async () => {
      try {
        const res = await api.get(`api/marriage/${spouseId}/detail/`);
        setInitialData({
          spouseName: res.data.spouse_name,
          phoneNumber: res.data.phone_number,
          address: res.data.address,
          registrationNumber: res.data.registration_number,
          marriageDate: res.data.marriage_date,
          marriagePlace: res.data.marriage_place,
          createdAt: res.data.date_added,
          createdBy: res.data.created_by_display,
          updatedAt: res.data.date_modified,
          updatedBy: res.data.updated_by_display,
        });
        setLoadingData(false);
      } catch (error) {
        if (error.response?.status === 404) {
          setResponse({
            message: "Spouse record not found",
            type: "error",
            id: Date.now(),
          });
          navigate(`/home/employees/${serviceId}/spouse`);
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
    fetchSpouse();
  }, []);

  const updateSpouse = async () => {
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
      const res = await api.patch(`api/marriage/${spouseId}/edit/`, payload);
      setFormData({
        spouseName: res.data.spouse_name,
        phoneNumber: res.data.phone_number,
        address: res.data.address,
        registrationNumber: res.data.registration_number,
        marriageDate: res.data.marriage_date,
        marriagePlace: res.data.marriage_place,
        createdAt: res.data.date_added,
        createdBy: res.data.created_by_display,
        updatedAt: res.data.date_modified,
        updatedBy: res.data.updated_by_display,
      });
      setResponse({
        message: "Spouse record updated",
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
      const res = await api.delete(`api/marriage/${spouseId}/delete/`);
      if (res.status === 204) {
        navigate(`/home/employees/${serviceId}/spouse`);
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
              onClick={() => navigate(`/home/employees/${serviceId}/spouse`)}
            >
              All Spouse
            </button>
          )}
        </div>
      </div>
      <div className={style.inputAndButtonsSection}>
        <SpouseInputBoxes
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
              <button onClick={updateSpouse}>
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
