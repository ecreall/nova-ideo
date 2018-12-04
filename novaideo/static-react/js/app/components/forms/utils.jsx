import React from 'react';
import { I18n } from 'react-redux-i18n';
import Checkbox from '@material-ui/core/Checkbox';
import Icon from '@material-ui/core/Icon';
import classNames from 'classnames';
import Tooltip from '@material-ui/core/Tooltip';
import Input from '@material-ui/core/Input';
import InputAdornment from '@material-ui/core/InputAdornment';
import { withStyles } from '@material-ui/core/styles';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControlLabel from '@material-ui/core/FormControlLabel';

import TextBoxField from './widgets/TextBoxField';
import FilesPicker from './widgets/FilesPicker';
import Select from './widgets/Select';
import SelectField from './widgets/SelectField';
import SelectList from './widgets/SelectList';
import MediumEditor from './widgets/mediumEditor/MediumEditor';
import Record from './widgets/Record';
import ImagePicker from './widgets/ImagePicker';

export const renderTextBoxField = ({
  input: { name, value, onChange },
  placeholder,
  onCtrlEnter,
  onEnter,
  autoFocus,
  style,
  withEmoji,
  initRef
}) => {
  return (
    <TextBoxField
      initRef={initRef}
      withEmoji={withEmoji}
      autoFocus={autoFocus}
      style={style}
      onEnter={onEnter}
      onCtrlEnter={onCtrlEnter}
      name={name}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
    />
  );
};

export const renderRichTextField = ({
  input: { name, value, onChange }, placeholder, autoFocus, initRef
}) => {
  return (
    <MediumEditor
      initRef={initRef}
      autoFocus={autoFocus}
      name={name}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
    />
  );
};

export const renderAnonymousCheckboxField = ({ input: { value, onChange }, classes }) => {
  const anonymous = Boolean(value);
  return (
    <Tooltip title={anonymous ? I18n.t('forms.disableAnonymity') : I18n.t('forms.remainAnonymous')} placement="top">
      <Checkbox
        icon={<Icon className="mdi-set mdi-guy-fawkes-mask" />}
        checkedIcon={<Icon className="mdi-set mdi-guy-fawkes-mask" />}
        value={value}
        onChange={onChange}
        classes={{
          root: classNames(classes.maskIcon, classes.maskDefault),
          checked: classNames(classes.maskIcon, classes.maskChecked)
        }}
      />
    </Tooltip>
  );
};

const checkboxStyles = (theme) => {
  return {
    error: {
      marginTop: -10,
      marginBottom: 10,
      paddingLeft: 5,
      fontSize: 11,
      color: theme.palette.danger.primary,
      fontWeight: 'bold'
    }
  };
};

export const renderCheckboxField = withStyles(checkboxStyles, {
  withTheme: true
})(({
  input: { value, onChange }, meta: { touched, error }, label, classes
}) => {
  return (
    <React.Fragment>
      <FormControlLabel control={<Checkbox value={value} onChange={onChange} />} label={label} />
      {touched && error ? (
        <FormHelperText className={classes.error} id={label}>
          {error}
        </FormHelperText>
      ) : null}
    </React.Fragment>
  );
});

export const renderFilesListField = ({ input: { value, onChange }, node, initRef }) => {
  return (
    <FilesPicker initRef={initRef} className="files-dropzone-list" value={value} onChange={onChange} multiple clickable>
      {node}
    </FilesPicker>
  );
};

export const renderImageField = ({
  input: { value, onChange }, initRef, label, helper
}) => {
  return <ImagePicker initRef={initRef} value={value} onChange={onChange} label={label} helper={helper} />;
};

export const renderRecordField = ({ input: { value, onChange }, node, initRef }) => {
  return (
    <Record initRef={initRef} value={value} onChange={onChange} multiple clickable>
      {node}
    </Record>
  );
};

export const renderSelect = ({
  input: { value, onChange }, options, label, canAdd, initRef
}) => {
  return <Select initRef={initRef} label={label} options={options} value={value} onChange={onChange} canAdd={canAdd} />;
};

export const renderSelectList = ({
  input: { value, onChange }, options, label, initRef
}) => {
  return <SelectList initRef={initRef} label={label} options={options} value={value} onChange={onChange} />;
};

export const renderSelectField = ({
  input: { name, value, onChange }, options, label, initRef
}) => {
  return <SelectField initRef={initRef} name={name} label={label} options={options} value={value} onChange={onChange} />;
};

const textInputStyles = (theme) => {
  return {
    root: {
      backgroundColor: 'white',
      border: '1px solid #a0a0a2',
      borderRadius: 4,
      boxShadow: 'inset 0 1px 1px rgba(0,0,0,.075)',
      alignItems: 'center',
      height: 45
    },
    multilineRoot: {
      height: 'auto !important',
      minHeight: 45,
      padding: '6px 0 23px 0'
    },
    errorRoot: {
      borderColor: theme.palette.danger.primary
    },
    container: {
      width: '100%',
      marginBottom: 10
    },
    input: {
      padding: '10px 10px 10px',
      fontSize: 15,
      width: 'calc(100% - 19px)',
      '&::placeholder': {
        color: '#000',
        fontSize: 15,
        fontWeight: 400,
        opacity: '.375'
      }
    },
    helper: {
      marginTop: 4,
      fontSize: 11
    },
    error: {
      marginTop: 4,
      paddingLeft: 5,
      fontSize: 11,
      color: theme.palette.danger.primary,
      fontWeight: 'bold'
    },
    label: {
      fontWeight: 'bold',
      margin: '0 0 .25rem',
      display: 'block',
      fontSize: 17
    },
    labelOptional: {
      fontWeight: '400 !important',
      color: '#717274 !important'
    },
    multiline: {
      minHeight: 20
    }
  };
};

export const renderTextInput = withStyles(textInputStyles, {
  withTheme: true
})(
  ({
    input: { name, value, onChange },
    meta: { touched, error },
    multiline,
    disabled,
    placeholder,
    endAdornment,
    endAdornmentPosition,
    label,
    helper,
    optional,
    autoFocus,
    type,
    autoComplete,
    classes
  }) => {
    return (
      <div className={classes.container}>
        {label && (
          <label className={classes.label} htmlFor={name}>
            {label}
            {optional && (
              <span className={classes.labelOptional}>
                {' '}
                {I18n.t('forms.optional')}
              </span>
            )}
          </label>
        )}
        <Input
          type={type || 'text'}
          autoComplete={autoComplete}
          autoFocus={autoFocus}
          fullWidth
          disableUnderline
          multiline={multiline}
          id={name}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          disabled={disabled}
          inputProps={{
            classes: {
              root: classNames({
                [classes.multiline]: multiline
              })
            }
          }}
          classes={{
            root: classNames(classes.root, {
              [classes.errorRoot]: touched && error,
              [classes.multilineRoot]: multiline
            }),
            input: classes.input
          }}
          endAdornment={<InputAdornment position={endAdornmentPosition}>{endAdornment}</InputAdornment>}
        />
        {helper && (
          <FormHelperText className={classes.helper} id={name}>
            {helper}
          </FormHelperText>
        )}
        {touched
          && error && (
          <FormHelperText className={classes.error} id={name}>
            {error}
          </FormHelperText>
        )}
      </div>
    );
  }
);