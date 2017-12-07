import React from 'react';

import InputField from './inputField';

export default class RadioField extends InputField {
  coerceValue(value) {
    return value ? true : false;
  }

  onChange = (value, onChange, onBlur, e) => {
    let newValue = this.coerceValue(!value);
    onChange(newValue, e);
    onBlur(newValue, e);
  };

  render() {
    return (
      <InputField
        {...this.props}
        field={({onChange, onBlur, value, disabled, ...props}) => (
          <div>
            {(props.choices() || []).map(choice => {
              return (
                <div key={choice[0]} value={choice[0]}>
                  {choice[1]}
                </div>
              );
            })}
          </div>
        )}
      />
    );
  }
}
