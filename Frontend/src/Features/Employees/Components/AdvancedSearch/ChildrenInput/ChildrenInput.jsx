import style from "../../../../../styles/components/advancedsearch.module.css";
import Dropdown from "../Dropdown";

export default function ChildrenInput() {
  return (
    <>
      <div className={style.recordTitle}>
        <i>Children</i>
      </div>
      <div className={style.dropdownContainer}>
        <Dropdown record={"Children"} />
      </div>
    </>
  );
}
