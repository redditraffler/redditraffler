import PropTypes from "prop-types";
import React from "react";
import { useFormContext, Controller } from "react-hook-form";

import {
  Field,
  Control,
  Input,
} from "react-bulma-components/lib/components/form";

interface InputWithStaticButtonProps {
  staticText: string;
  inputType: "text" | "number";
  name: string;
}

/**
 * A form field group containing an input with an adjacent static button.
 * The input is wrapped with the RHF Controller component.
 */
const InputWithStaticButton: React.FC<InputWithStaticButtonProps> = ({
  staticText,
  inputType,
  name,
}) => {
  const { control } = useFormContext();

  return (
    <Field kind="addons">
      <Control>
        <Controller name={name} control={control} as={Input} type={inputType} />
      </Control>
      <Control>
        <span className="button is-static">{staticText}</span>
      </Control>
    </Field>
  );
};

InputWithStaticButton.propTypes = {
  staticText: PropTypes.string.isRequired,
  inputType: PropTypes.oneOf(["text", "number"] as const).isRequired,
  name: PropTypes.string.isRequired,
};

export default InputWithStaticButton;
