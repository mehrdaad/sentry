import React from 'react';
import InputField from './inputField';

export default class RadioField extends InputField {
  onChange = (value, onChange, onBlur, e) => {
    onChange(value, e);
    onBlur(value, e);
  };

  isSelected = ({value, id}) => {
    return value ? value === id : id === 0;
  };

  render() {
    return (
      <InputField
        {...this.props}
        field={({onChange, onBlur, value, disabled, ...props}) => (
          <div>
            {(props.choices() || []).map(choice => {
              const {id, name} = choice;
              return (
                <div
                  key={id}
                  value={id}
                  onClick={this.onChange.bind(this, id, onChange, onBlur)}
                  style={{fontWeight: this.isSelected({value, id}) ? 'bold' : 'inherit'}}
                >
                  {name}
                </div>
              );
            })}
          </div>
        )}
      />
    );
  }
}
