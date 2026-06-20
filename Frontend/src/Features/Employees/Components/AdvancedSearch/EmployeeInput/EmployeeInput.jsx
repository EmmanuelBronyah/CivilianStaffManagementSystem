import style from "../../../../../styles/components/advancedsearch.module.css";
import Dropdown from "../Dropdown";

export default function EmployeeInput(props) {
  return (
    <>
      <div className={style.recordTitle}>
        <i>Employee</i>
      </div>
      <div className={style.dropdownContainer}>
        <Dropdown record={"Employee"} setDropdownData={props.setDropdownData} />
      </div>
    </>
  );
}
