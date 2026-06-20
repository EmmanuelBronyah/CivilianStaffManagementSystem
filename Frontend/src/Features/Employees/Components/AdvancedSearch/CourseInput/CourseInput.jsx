import style from "../../../../../styles/components/advancedsearch.module.css";
import Dropdown from "../Dropdown";

export default function CourseInput() {
  return (
    <>
      <div className={style.recordTitle}>
        <i>Course</i>
      </div>
      <div className={style.dropdownContainer}>
        <Dropdown record={"Course"} />
      </div>
    </>
  );
}
