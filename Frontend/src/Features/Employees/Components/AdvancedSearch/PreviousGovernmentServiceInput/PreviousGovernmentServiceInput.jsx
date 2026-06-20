import style from "../../../../../styles/components/advancedsearch.module.css";
import Dropdown from "../Dropdown";

export default function PreviousGovernmentServiceInput() {
  return (
    <>
      <div className={style.recordTitle}>
        <i>Previous Government Service</i>
      </div>
      <div className={style.dropdownContainer}>
        <Dropdown record={"Previous Government Service"} />
      </div>
    </>
  );
}
