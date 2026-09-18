import style from "../../../../styles/components/advancedsearch.module.css";
import Dropdown from "./Dropdown";
import { useEffect, useState } from "react";
import InputBox from "./InputBox";
import RangeInputBox from "./RangeInputBox";

export default function ParentInput(props) {
  const [dropdownData, setDropdownData] = useState(null);
  const [rangeOption, setRangeOption] = useState(null);
  const [fieldErrors, setFieldErrors] = useState(null);

  useEffect(() => {
    setDropdownData(null);
    setRangeOption(null);
    setFieldErrors(null);
  }, [props.record]);

  useEffect(() => {
    setRangeOption(null);
    setFieldErrors(null);
  }, [dropdownData]);
  return (
    <>
      <div className={style.recordTitle}>
        <i>{props.record}</i>
      </div>
      <div className={style.dropdownContainer}>
        <Dropdown
          record={props.record}
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
            record={props.record}
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
            record={props.record}
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
