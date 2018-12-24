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
import DatePicker from 'react-datepicker';
import Moment from 'moment';

import TextBoxField from './widgets/TextBoxField';
import FilesPicker from './widgets/FilesPicker';
import Select from './widgets/Select';
import CardSelect from './widgets/CardSelect';
import SelectField from './widgets/SelectField';
import SelectList from './widgets/SelectList';
import MediumEditor from './widgets/mediumEditor/MediumEditor';
import Record from './widgets/Record';
import ImagePicker from './widgets/ImagePicker';
import RichSelect from './widgets/richSelect/RichSelect';

export const renderTextBoxField = ({ input: { name, value, onChange }, ...props }) => {
  return <TextBoxField {...props} name={name} value={value} onChange={onChange} />;
};

export const renderRichTextField = ({ input: { name, value, onChange }, ...props }) => {
  return <MediumEditor {...props} name={name} value={value} onChange={onChange} />;
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
  input: { name, value, onChange }, meta: { touched, error }, label, classes
}) => {
  return (
    <React.Fragment>
      <FormControlLabel control={<Checkbox value={value} onChange={onChange} />} label={label} />
      {touched && error ? (
        <FormHelperText className={classes.error} id={name}>
          {error}
        </FormHelperText>
      ) : null}
    </React.Fragment>
  );
});

export const renderFilesListField = ({ input: { value, onChange }, node, ...props }) => {
  return (
    <FilesPicker {...props} className="files-dropzone-list" value={value} onChange={onChange} multiple clickable>
      {node}
    </FilesPicker>
  );
};

export const renderImageField = ({ input: { value, onChange }, ...props }) => {
  return <ImagePicker {...props} value={value} onChange={onChange} />;
};

export const renderRecordField = ({ input: { value, onChange }, node, initRef }) => {
  return (
    <Record initRef={initRef} value={value} onChange={onChange} multiple clickable>
      {node}
    </Record>
  );
};

export const renderSelect = ({ input: { value, onChange }, ...props }) => {
  return <Select {...props} value={value} onChange={onChange} />;
};

export const renderCardSelect = ({ input: { name, value, onChange }, ...props }) => {
  return <CardSelect {...props} name={name} value={value} onChange={onChange} />;
};

export const renderSelectList = ({ input: { value, onChange }, ...props }) => {
  return <SelectList {...props} value={value} onChange={onChange} />;
};

export const renderRichSelect = ({ input: { value, onChange }, ...props }) => {
  return <RichSelect {...props} value={value} onChange={onChange} />;
};

export const renderSelectField = ({ input: { name, value, onChange }, ...props }) => {
  return <SelectField {...props} name={name} value={value} onChange={onChange} />;
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
      width: 'calc(100% - 20px)',
      minHeight: 20,
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
    endAdornment,
    endAdornmentPosition,
    label,
    helper,
    optional,
    type,
    classes,
    multiline,
    ...props
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
          {...props}
          type={type || 'text'}
          fullWidth
          disableUnderline
          multiline={multiline}
          id={name}
          value={value}
          onChange={onChange}
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

export const renderDatePicker = withStyles(textInputStyles, {
  withTheme: true
})(({
  input: { name, value, onChange }, meta: { touched, error }, label, helper, optional, classes, placeholder, ...props
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
      <DatePicker
        {...props}
        placeholderText={placeholder}
        selected={value ? Moment(value) : null}
        onChange={onChange}
        locale="fr"
        className={classes.root}
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
});