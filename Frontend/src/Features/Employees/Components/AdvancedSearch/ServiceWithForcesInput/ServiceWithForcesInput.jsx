import style from "../../../../../styles/components/advancedsearch.module.css";
import Dropdown from "../Dropdown";

export default function ServiceWithForcesInput() {
  return (
    <>
      <div className={style.recordTitle}>
        <i>Service With Forces</i>
      </div>
      <div className={style.dropdownContainer}>
        <Dropdown record={"Service With Forces"} />
      </div>
    </>
  );
}
