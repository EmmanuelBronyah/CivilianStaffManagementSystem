import { useEffect } from "react";
import style from "../../../../styles/components/advancedsearch.module.css";
import { inputRecordData, allLabelKeys, rangeLabelKey } from "./constants";

export default function RangeInputBox(props) {
  const inputData = inputRecordData[props.record].find(
    ([label]) => props.dropdownLabel === label,
  );
  const [, inputType] = inputData || [];

  const isDigitsOnlyField = (label) => {
    const fieldLabels = ["Age", "Probation"];
    return fieldLabels.includes(label);
  };

  const from =
    props.formData?.[props.record]?.[allLabelKeys[props.dropdownLabel]]?.between
      ?.from ?? "";

  const to =
    props.formData?.[props.record]?.[allLabelKeys[props.dropdownLabel]]?.between
      ?.to ?? "";

  useEffect(() => {
    if (from === "" || to === "") {
      props.setFieldErrors(null);
      return;
    }

    const isDateField = props.dropdownLabel.toLowerCase().includes("date");

    if (isDateField) {
      const fromDate = new Date(from);
      const toDate = new Date(to);

      if (fromDate > toDate) {
        props.setFieldErrors(
          "From Date field cannot be greater than the To Date field.",
        );
      } else {
        props.setFieldErrors(null);
      }
    } else {
      if (Number(from) > Number(to)) {
        props.setFieldErrors(
          "From field value cannot be greater than the To field value.",
        );
      } else {
        props.setFieldErrors(null);
      }
    }
  }, [from, to]);

  const updateBetweenValue = (field, value) => {
    props.setFormData((prev) => ({
      ...prev,
      [props.record]: {
        ...prev[props.record],
        [allLabelKeys[props.dropdownLabel]]: {
          between: {
            ...prev[props.record]?.[allLabelKeys[props.dropdownLabel]]?.between,
            [field]: value,
          },
        },
      },
    }));
  };

  if (props.rangeLabel === "Between") {
    return (
      <div key={props.rangeLabel} className={style.betweenRangeContainer}>
        <div>
          <div>
            <i>From</i>
          </div>
          <input
            type={inputType}
            {...(inputType === "number" && { step: 1, min: 0 })}
            value={
              props.formData?.[props.record]?.[
                allLabelKeys[props.dropdownLabel]
              ]?.between?.from ?? ""
            }
            onChange={(e) => {
              if (
                isDigitsOnlyField(props.dropdownLabel) &&
                !/^\d*$/.test(e.target.value)
              ) {
                return;
              }
              props.setFieldErrors(null);
              updateBetweenValue("from", e.target.value);
            }}
          />
        </div>
        <div>
          <div>
            <i>To</i>
          </div>
          <input
            type={inputType}
            {...(inputType === "number" && { step: 1, min: 0 })}
            value={
              props.formData?.[props.record]?.[
                allLabelKeys[props.dropdownLabel]
              ]?.between?.to ?? ""
            }
            onChange={(e) => {
              if (
                isDigitsOnlyField(props.dropdownLabel) &&
                !/^\d*$/.test(e.target.value)
              ) {
                return;
              }

              props.setFieldErrors(null);
              updateBetweenValue("to", e.target.value);
            }}
          />
        </div>
      </div>
    );
  } else {
    return (
      <div key={props.rangeLabel} className={style.singleChoiceContainer}>
        <input
          type={inputType}
          {...(inputType === "number" && { step: 1, min: 0 })}
          value={
            props.formData?.[props.record]?.[
              allLabelKeys[props.dropdownLabel]
            ]?.[rangeLabelKey[props.rangeLabel]] ?? ""
          }
          onChange={(e) => {
            if (
              isDigitsOnlyField(props.dropdownLabel) &&
              !/^\d*$/.test(e.target.value)
            ) {
              return;
            }
            props.setFieldErrors(null);
            props.setFormData((prev) => ({
              ...prev,
              [props.record]: {
                ...prev[props.record],
                [allLabelKeys[props.dropdownLabel]]: {
                  [rangeLabelKey[props.rangeLabel]]: e.target.value,
                },
              },
            }));
          }}
        />
      </div>
    );
  }
}
