import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import PrimaryComponentInputBoxes from "./InputBoxesPrimaryComponent";
import { useEffect, useState } from "react";
import api from "../../../../api";
import useFetchUserRole from "../../../hooks/fetchUserRoleHook";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import ClipLoader from "react-spinners/ClipLoader";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import { useOutletContext, useParams } from "react-router-dom";
import { MdDelete } from "react-icons/md";
import verifyAdminProcess from "../../../../utils/askAdminIdentity";
import { showErrorModal } from "../../../../utils/askAdminIdentity";
import askToDelete from "../../../../utils/askToDelete";
import { useNavigate } from "react-router-dom";

export default function EmployeePrimary() {
  const { role, response } = useFetchUserRole();
  const [loadingData, setLoadingData] = useState(true);
  const [loading, setLoading] = useState(false);
  const [loadingDeletion, setLoadingDeletion] = useState(false);
  const { theme } = useTheme();
  const { serviceId } = useParams();
  const {
    setHeaderData,
    initialData,
    setInitialData,
    formData,
    setFormData,
    setResponse,
  } = useOutletContext();
  const navigate = useNavigate();

  useEffect(() => {
    if (!response) return;
    setResponse(response);
  });

  const FIELD_MAP = {
    serviceId: "service_id",
    lastName: "last_name",
    otherNames: "other_names",
    address: "address",
    appointmentDate: "appointment_date",
    confirmationDate: "confirmation_date",
    bloodGroup: "blood_group",
    category: "category",
    disable: "disable",
    dob: "dob",
    age: "age",
    email: "email",
    entryQualification: "entry_qualification",
    gender: "gender",
    grade: "grade",
    hometown: "hometown",
    maritalStatus: "marital_status",
    nationality: "nationality",
    probation: "probation",
    region: "region",
    religion: "religion",
    socialSecurity: "social_security",
    station: "station",
    structure: "structure",
    unit: "unit",
  };

  function getChangedFields(initialData, formData) {
    const payload = {};

    for (const key in formData) {
      const initialValue = initialData[key];
      const currentValue = formData[key];

      const normalizedInitial =
        initialValue && typeof initialValue === "object"
          ? initialValue.value
          : initialValue;

      const normalizedCurrent =
        currentValue && typeof currentValue === "object"
          ? currentValue.value
          : currentValue;

      if (normalizedInitial !== normalizedCurrent) {
        payload[key] = normalizedCurrent;
      }
    }

    return payload;
  }

  const updateEmployee = async () => {
    setLoading(true);
    try {
      const changedFields = getChangedFields(initialData, formData);

      const payload = {};

      for (const key in changedFields) {
        const backendKey = FIELD_MAP[key];
        if (!backendKey) continue;

        let value = changedFields[key];

        if (typeof value === "string") {
          value = value.trim();
          if (value === "") value = null;
        }

        payload[backendKey] = value;
      }

      const serviceId = initialData.serviceId;

      const res = await api.patch(
        `api/employees/staff/${serviceId}/edit/`,
        payload,
      );
      setHeaderData({
        serviceId: res.data.service_id,
        lastName: res.data.last_name,
        otherNames: res.data.other_names,
        age: res.data.age,
      });
      setInitialData({
        serviceId: res.data.service_id,
        lastName: res.data.last_name,
        otherNames: res.data.other_names,
        address: res.data.address,
        appointmentDate: res.data.appointment_date,
        confirmationDate: res.data.confirmation_date,
        bloodGroup: {
          value: res.data.blood_group,
          label: res.data.blood_group_display,
        },
        category: res.data.category,
        disable: res.data.disable,
        dob: res.data.dob,
        age: res.data.age,
        email: res.data.email,
        entryQualification: res.data.entry_qualification,
        gender: {
          value: res.data.gender,
          label: res.data.gender_display,
        },
        grade: {
          value: res.data.grade,
          label: res.data.grade_display,
        },
        hometown: res.data.hometown,
        maritalStatus: {
          value: res.data.marital_status,
          label: res.data.marital_status_display,
        },
        nationality: res.data.nationality,
        probation: res.data.probation,
        region: {
          value: res.data.region,
          label: res.data.region_display,
        },
        religion: {
          value: res.data.religion,
          label: res.data.religion_display,
        },
        socialSecurity: res.data.social_security,
        station: res.data.station,
        structure: {
          value: res.data.structure,
          label: res.data.structure_display,
        },
        unit: {
          value: res.data.unit,
          label: res.data.unit_display,
        },
        createdAt: res.data.created_at,
        updatedAt: res.data.updated_at,
        createdBy: res.data.created_by_display,
        updatedBy: res.data.updated_by_display,
      });
      setLoading(false);
      setResponse({
        message: "Employee changes saved",
        id: Date.now(),
      });
      return;
    } catch (error) {
      setInitialData(initialData);
      setLoading(false);
      setResponse({
        message: getResponseMessages(error.response),
        type: "error",
        id: Date.now(),
      });
      return;
    }
  };

  const resetData = () => {
    setInitialData({
      serviceId: initialData.serviceId,
      lastName: initialData.lastName,
      otherNames: initialData.otherNames,
      address: initialData.address,
      appointmentDate: initialData.appointmentDate,
      confirmationDate: initialData.confirmationDate,
      bloodGroup: {
        value: initialData.bloodGroup.value,
        label: initialData.bloodGroup.label,
      },
      category: initialData.category,
      disable: initialData.disable,
      dob: initialData.dob,
      age: initialData.age,
      email: initialData.email,
      entryQualification: initialData.entryQualification,
      gender: {
        value: initialData.gender.value,
        label: initialData.gender.label,
      },
      grade: {
        value: initialData.grade.value,
        label: initialData.grade.label,
      },
      hometown: initialData.hometown,
      maritalStatus: {
        value: initialData.maritalStatus.value,
        label: initialData.maritalStatus.label,
      },
      nationality: initialData.nationality,
      probation: initialData.probation,
      region: {
        value: initialData.region.value,
        label: initialData.region.label,
      },
      religion: {
        value: initialData.religion.value,
        label: initialData.religion.label,
      },
      socialSecurity: initialData.socialSecurity,
      station: initialData.station,
      structure: {
        value: initialData.structure.value,
        label: initialData.structure.label,
      },
      unit: {
        value: initialData.unit.value,
        label: initialData.unit.label,
      },
      createdAt: formData.createdAt,
      updatedAt: formData.updatedAt,
      createdBy: formData.createdBy,
      updatedBy: formData.updatedBy,
    });
  };

  const initiateDeletion = async () => {
    const result = await askToDelete(theme);
    if (!result.isConfirmed) return;

    const status = await verifyAdminProcess(
      theme,
      setLoadingDeletion,
      setResponse,
    );

    if (status === 401) {
      await showErrorModal(theme);
      return;
    } else if (status === 200) {
      try {
        const res = await api.delete(
          `api/employees/staff/${serviceId}/delete/`,
        );
        if (res.status === 204) {
          setLoading(false);
          setResponse({
            message: "Employee record deleted",
            id: Date.now(),
          });
          setTimeout(() => {
            navigate("/home/employees");
          }, 3000);
        }
      } catch (error) {
        setLoading(false);
        setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
        return;
      }
    }
  };

  return (
    <div className={`${style.employeePrimary} ${!theme ? style.dark : ""}`}>
      <div className={style.inputs}>
        <PrimaryComponentInputBoxes
          loadingData={loadingData}
          setLoadingData={setLoadingData}
          formData={formData}
          setFormData={setFormData}
          setResponse={setResponse}
        />
      </div>
      {!role ? (
        <BaseSkeleton height={38} />
      ) : (
        <div
          className={`${style.buttons} ${role === "VIEWER" && style.displayNone}`}
        >
          <div className={style.emptyDiv}></div>
          <div className={style.saveCancelButtons}>
            {loadingData ? (
              <BaseSkeleton height={40} width={140} />
            ) : (
              <button
                disabled={loading || loadingDeletion}
                className={style.saveButton}
                onClick={updateEmployee}
              >
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
              <BaseSkeleton height={40} width={140} />
            ) : (
              <button
                onClick={resetData}
                className={style.cancelButton}
                disabled={loading || loadingDeletion}
              >
                Cancel
              </button>
            )}
          </div>

          {loadingData ? (
            <BaseSkeleton width={40} />
          ) : loadingDeletion ? (
            <ClipLoader size={30} color="#a30008" />
          ) : (
            <MdDelete
              className={`${style.trashIcon} ${!role || role === "VIEWER" ? style.displayNone : ""}`}
              onClick={initiateDeletion}
            />
          )}
        </div>
      )}
    </div>
  );
}
