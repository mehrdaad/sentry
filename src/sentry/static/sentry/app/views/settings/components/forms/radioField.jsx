import React from 'react';
import styled from 'react-emotion';
import PropTypes from 'prop-types';

import InputField from './inputField';

class RadioField extends InputField {
  static propTypes = {
    id: PropTypes.integer,
    value: PropTypes.string,
  };

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
                <RadioLineItem
                  key={id}
                  onClick={this.onChange.bind(this, id, onChange, onBlur)}
                >
                  <RadioLineButton>
                    {this.isSelected({value, id}) ? <RadioLineButtonFill /> : ''}
                  </RadioLineButton>
                  <RadioLineText>{name}</RadioLineText>
                </RadioLineItem>
              );
            })}
          </div>
        )}
      />
    );
  }
}

const RadioLineItem = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 0.5em;
  cursor: pointer;
`;

const RadioLineButton = styled.div`
  width: 1.5em;
  height: 1.5em;
  position: relative;
  border-radius: 50%;
  border: 1px solid ${p => p.theme.borderLight};
  box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.04);
`;

const RadioLineButtonFill = styled.div`
  width: 54%;
  height: 54%;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  background-color: ${p => p.theme.green};
`;

const RadioLineText = styled.div`
  margin-left: 0.5em;
  font-size: 0.875em;
  font-weight: bold;
`;

export default RadioField;
