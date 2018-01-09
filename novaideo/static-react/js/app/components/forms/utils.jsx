import React from 'react';
import Checkbox from 'material-ui/Checkbox';

import TextField from './widgets/TextField';

export const renderInput = ({ input: { name, value, onChange }, placeholder, placeholderTextColor }) => {
  return (
    <TextField
      name={name}
      placeholder={placeholder}
      placeholderTextColor={placeholderTextColor}
      value={value}
      onChange={onChange}
    />
  );
};
//
// export const renderFilesList = ({ input: { value, onChange }, navigation }) => {
//   return <FilesList navigation={navigation} value={value} onChange={onChange} />;
// };
//
// export const renderSelect = ({ input: { name, value, onChange }, options, label, canAdd, errors, displayErrors, style }) => {
//   const hasError = displayErrors && errors && name in errors;
//   const inputStyle = style || { labelColor: '#a2a4a2ff' };
//   const labelColor = hasError ? '#f00' : inputStyle.labelColor || '#a2a4a2ff';
//   return (
//     <Select
//       options={options}
//       label={hasError ? errors[name] : label}
//       labelColor={labelColor}
//       canAdd={canAdd}
//       value={value || []}
//       onChange={onChange}
//     />
//   );
// };

export const renderCheckbox = ({ input: { value, onChange }, label }) => {
  return (
    <Checkbox
      iconSize={15}
      styleText={{
        color: 'gray',
        marginLeft: 4,
        fontSize: 15
      }}
      styleIcon={{
        marginTop: 2
      }}
      iconColor="gray"
      label={label}
      value={value}
      onChange={onChange}
    />
  );
};