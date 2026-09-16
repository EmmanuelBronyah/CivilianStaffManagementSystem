import style from "../../../../../styles/components/advancedsearch.module.css";
import Dropdown from "../Dropdown";
import { useEffect, useState } from "react";
import InputBox from "../InputBox";
import RangeInputBox from "../RangeInputBox";

export default function ServiceWithForcesInput(props) {
  const [dropdownData, setDropdownData] = useState(null);
  const [rangeOption, setRangeOption] = useState(null);
  const [fieldErrors, setFieldErrors] = useState(null);

  useEffect(() => {
    setRangeOption(null);
  }, [dropdownData]);

  return (
    <>
      <div className={style.recordTitle}>
        <i>Service With Forces</i>
      </div>
      <div className={style.dropdownContainer}>
        <Dropdown
          record="Service With Forces"
          dropdownData={dropdownData}
          setDropdownData={setDropdownData}
        />
      </div>
      {dropdownData?.label && (
        /* the input box that pops down when a user selects either Service ID,
          etc from the first dropdown */
        <>
          {fieldErrors && (
            <div className={style.errorMessage}>
              <p>{fieldErrors}</p>
            </div>
          )}

          <InputBox
            record="Service With Forces"
            label={dropdownData?.label}
            formData={props.formData}
            setFormData={props.setFormData}
            rangeOption={rangeOption}
            setRangeOption={setRangeOption}
          />
        </>
      )}
      {rangeOption?.label && (
        <>
          <RangeInputBox
            record="Service With Forces"
            rangeLabel={rangeOption?.label}
            dropdownLabel={dropdownData?.label}
            formData={props.formData}
            setFormData={props.setFormData}
            setFieldErrors={setFieldErrors}
          />
        </>
      )}
    </>
  );
}
