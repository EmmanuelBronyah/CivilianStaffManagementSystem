import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import CoursesInputBoxes from "./CoursesInputBoxesComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import ClipLoader from "react-spinners/ClipLoader";
import useFetchUserRole from "../../../hooks/fetchUserRoleHook";

export default function AddCourses() {
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const { theme } = useTheme();
  const navigate = useNavigate();
  const { serviceId } = useParams();
  const { setResponse } = useOutletContext();

  const { role, response } = useFetchUserRole();

  useEffect(() => {
    if (!response) return;
    setResponse(response);
  });

  const addCourse = async () => {
    setLoading(true);

    const payload = {
      employee: serviceId,
      course_type: formData.courseType,
      place: formData.place,
      date_commenced: formData.dateCommenced || null,
      date_ended: formData.dateEnded || null,
      qualification: formData.qualification,
      result: formData.result,
      authority: formData.authority,
    };

    try {
      const res = await api.post("api/courses/create/", payload);
      setFormData({
        courseType: res.data.course_type,
        place: res.data.place,
        dateCommenced: res.data.date_commenced,
        dateEnded: res.data.date_ended,
        qualification: res.data.qualification,
        result: res.data.result,
        authority: res.data.authority,
      });
      setResponse({
        message: "Course saved",
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
            onClick={() => navigate(`/home/employees/${serviceId}/courses`)}
          >
            All Courses
          </button>
        </div>
      </div>
      <div className={style.inputAndButtonsSection}>
        <CoursesInputBoxes
          formData={formData}
          setFormData={setFormData}
          setResponse={setResponse}
        />
        <div className={style.addOccurrenceButtons}>
          <div className={style.addCancelButtons}>
            <button
              onClick={addCourse}
              className={!role || role === "VIEWER" ? style.displayNone : ""}
            >
              {loading ? (
                <ClipLoader
                  size={13}
                  color={`${!theme ? "#1e1e1e" : "#d7fdd7"}`}
                />
              ) : (
                "Save Course Record"
              )}
            </button>
            <button
              className={`${style.cancelButton} ${!role || role === "VIEWER" ? style.displayNone : ""}`}
              onClick={() => navigate(`/home/employees/${serviceId}/courses`)}
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
