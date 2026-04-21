import style from "../../../styles/components/employees.module.css";
import { useTheme } from "../../../context/ThemeContext";
import PrimaryComponentInputBoxes from "./InputBoxesPrimaryComponent";
import { useEffect, useState } from "react";
import api from "../../../api";
import { USER_ID } from "../../../constants";
import useFetchUserRole from "../../hooks/fetchUserRoleHook";
import getResponseMessages from "../../../utils/extractResponseMessage";
import ClipLoader from "react-spinners/ClipLoader";

export default function EmployeePrimary(props) {
  const { role, response } = useFetchUserRole();
  const [loadingData, setLoadingData] = useState(true);
  const [loading, setLoading] = useState(false);
  const { theme } = useTheme();

  useEffect(() => {
    if (!response) return;
    props.setResponse(response);
  });

  const updateEmployee = async () => {
    setLoading(true);
    try {
      console.log("formData -> ", props.formData);

      const serviceId = props.initialData.serviceId;
      const payload = {
        service_id: props.formData.serviceId.trim(),
        last_name: props.formData.lastName.trim(),
        other_names: props.formData.otherNames.trim(),
        address: props.formData.address.trim(),
        appointment_date: props.formData.appointmentDate,
        confirmation_date: props.formData.confirmationDate,
        blood_group: props.formData.bloodGroup.value,
        category: props.formData.category.trim(),
        disable: props.formData.disable,
        dob: props.formData.dob || null,
        email: props.formData.email.trim(),
        entry_qualification: props.formData.entryQualification.trim(),
        gender: props.formData.gender.value,
        grade: props.formData.grade.value,
        hometown: props.formData.hometown.trim(),
        marital_status: props.formData.maritalStatus.value,
        nationality: props.formData.nationality.trim(),
        probation: props.formData.probation.trim(),
        region: props.formData.region.value,
        religion: props.formData.religion.value,
        social_security: props.formData.socialSecurity.trim(),
        station: props.formData.station.trim(),
        structure: props.formData.structure.value,
        unit: props.formData.unit.value,
      };
      const res = await api.patch(
        `api/employees/staff/${serviceId}/edit/`,
        payload,
      );
      console.log("Edit Response data -> ", res.data, res.status);
      props.setHeaderData({
        serviceId: res.data.service_id,
        lastName: res.data.last_name,
        otherNames: res.data.other_names,
        age: res.data.age,
      });
      props.setInitialData({
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
        createdBy: res.data.created_by_display,
        updatedBy: res.data.updated_by_display,
      });
      setLoading(false);
      props.setResponse({
        message: "Employee changes saved",
        id: Date.now(),
      });
      return;
    } catch (error) {
      console.log("initial data -> ", props.initialData);

      props.setInitialData(props.initialData);
      setLoading(false);
      props.setResponse({
        message: getResponseMessages(error.response),
        type: "error",
        id: Date.now(),
      });
      return;
    }
  };
  return (
    <div className={`${style.employeePrimary} ${!theme ? style.dark : ""}`}>
      <div className={style.inputs}>
        <PrimaryComponentInputBoxes
          formData={props.formData}
          setFormData={props.setFormData}
          setResponse={props.setResponse}
        />
      </div>
      <div
        className={`${style.buttons} ${role && role === "VIEWER" && style.displayNone}`}
      >
        <button
          disabled={loading}
          className={style.saveButton}
          onClick={updateEmployee}
        >
          {loading ? (
            <ClipLoader size={13} color={`${!theme ? "#1e1e1e" : "#d7fdd7"}`} />
          ) : (
            "Save Changes"
          )}
        </button>
        <button className={style.cancelButton} disabled={loading}>
          Cancel
        </button>
      </div>
    </div>
  );
}
