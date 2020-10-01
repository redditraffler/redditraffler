import PropTypes from "prop-types";
import React from "react";
import { useFormContext, Controller } from "react-hook-form";
import {
  Field,
  Control,
  Input,
  Label,
} from "react-bulma-components/lib/components/form";

import { colors } from "@js/theme";

interface InputWithStaticButtonProps extends Partial<HTMLInputElement> {
  label?: string;
  staticText: string;
  inputType: "text" | "number";
  name: string;
}

/**
 * A form field group containing an input with an adjacent static button.
 * The input is wrapped with the RHF Controller component.
 */
const InputWithStaticButton: React.FC<InputWithStaticButtonProps> = ({
  label,
  staticText,
  inputType,
  name,
  ...props
}) => {
  const { control } = useFormContext();

  return (
    <React.Fragment>
      <Label style={{ color: colors.reddit }}>{label}</Label>
      <Field kind="addons">
        <Control>
          <Controller
            name={name}
            control={control}
            as={Input}
            type={inputType}
            {...props}
          />
        </Control>
        <Control>
          <span className="button is-static">{staticText}</span>
        </Control>
      </Field>
    </React.Fragment>
  );
};

InputWithStaticButton.propTypes = {
  label: PropTypes.string,
  staticText: PropTypes.string.isRequired,
  inputType: PropTypes.oneOf(["text", "number"] as const).isRequired,
  name: PropTypes.string.isRequired,
};

export default InputWithStaticButton;
