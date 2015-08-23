function varargout = SFCoffeeShopRandomizer(varargin)
% SFCOFFEESHOPRANDOMIZER M-file for SFCoffeeShopRandomizer.fig
%      SFCOFFEESHOPRANDOMIZER, by itself, creates a new SFCOFFEESHOPRANDOMIZER or raises the existing
%      singleton*.
%
%      H = SFCOFFEESHOPRANDOMIZER returns the handle to a new SFCOFFEESHOPRANDOMIZER or the handle to
%      the existing singleton*.
%
%      SFCOFFEESHOPRANDOMIZER('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in SFCOFFEESHOPRANDOMIZER.M with the given input arguments.
%
%      SFCOFFEESHOPRANDOMIZER('Property','Value',...) creates a new SFCOFFEESHOPRANDOMIZER or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before SFCoffeeShopRandomizer_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to SFCoffeeShopRandomizer_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help SFCoffeeShopRandomizer

% Last Modified by GUIDE v2.5 23-Aug-2013 17:04:53

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @SFCoffeeShopRandomizer_OpeningFcn, ...
                   'gui_OutputFcn',  @SFCoffeeShopRandomizer_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before SFCoffeeShopRandomizer is made visible.
function SFCoffeeShopRandomizer_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to SFCoffeeShopRandomizer (see VARARGIN)

% Choose default command line output for SFCoffeeShopRandomizer
handles.output = hObject;
handles.this = hObject;

%load up the database
handles.databasefile = 'sfcoffeeshops.mat';
handles = loadDatabaseFromFile(handles);

%choose an initial shop -completely- randomly
handles.databaseidx = ceil(rand(1)*handles.nshops);
handles = showEntry(handles, handles.databaseidx);


% Update handles structure
guidata(hObject, handles);

% UIWAIT makes SFCoffeeShopRandomizer wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = SFCoffeeShopRandomizer_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;



function shopname_text_Callback(hObject, eventdata, handles)
% hObject    handle to shopname_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of shopname_text as text
%        str2double(get(hObject,'String')) returns contents of shopname_text as a double


% --- Executes during object creation, after setting all properties.
function shopname_text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to shopname_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function location_text_Callback(hObject, eventdata, handles)
% hObject    handle to location_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of location_text as text
%        str2double(get(hObject,'String')) returns contents of location_text as a double


% --- Executes during object creation, after setting all properties.
function location_text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to location_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function tuesopen_text_Callback(hObject, eventdata, handles)
% hObject    handle to tuesopen_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of tuesopen_text as text
%        str2double(get(hObject,'String')) returns contents of tuesopen_text as a double


% --- Executes during object creation, after setting all properties.
function tuesopen_text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to tuesopen_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function tuesclose_text_Callback(hObject, eventdata, handles)
% hObject    handle to tuesclose_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of tuesclose_text as text
%        str2double(get(hObject,'String')) returns contents of tuesclose_text as a double


% --- Executes during object creation, after setting all properties.
function tuesclose_text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to tuesclose_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function wedsclose_text_Callback(hObject, eventdata, handles)
% hObject    handle to wedsclose_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of wedsclose_text as text
%        str2double(get(hObject,'String')) returns contents of wedsclose_text as a double


% --- Executes during object creation, after setting all properties.
function wedsclose_text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to wedsclose_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function thursclose_text_Callback(hObject, eventdata, handles)
% hObject    handle to thursclose_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of thursclose_text as text
%        str2double(get(hObject,'String')) returns contents of thursclose_text as a double


% --- Executes during object creation, after setting all properties.
function thursclose_text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to thursclose_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function friopen_text_Callback(hObject, eventdata, handles)
% hObject    handle to friopen_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of friopen_text as text
%        str2double(get(hObject,'String')) returns contents of friopen_text as a double


% --- Executes during object creation, after setting all properties.
function friopen_text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to friopen_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function wedsopen_text_Callback(hObject, eventdata, handles)
% hObject    handle to wedsopen_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of wedsopen_text as text
%        str2double(get(hObject,'String')) returns contents of wedsopen_text as a double


% --- Executes during object creation, after setting all properties.
function wedsopen_text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to wedsopen_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function thursopen_text_Callback(hObject, eventdata, handles)
% hObject    handle to thursopen_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of thursopen_text as text
%        str2double(get(hObject,'String')) returns contents of thursopen_text as a double


% --- Executes during object creation, after setting all properties.
function thursopen_text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to thursopen_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function friclose_text_Callback(hObject, eventdata, handles)
% hObject    handle to friclose_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of friclose_text as text
%        str2double(get(hObject,'String')) returns contents of friclose_text as a double


% --- Executes during object creation, after setting all properties.
function friclose_text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to friclose_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function satopen_text_Callback(hObject, eventdata, handles)
% hObject    handle to satopen_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of satopen_text as text
%        str2double(get(hObject,'String')) returns contents of satopen_text as a double


% --- Executes during object creation, after setting all properties.
function satopen_text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to satopen_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function satclose_text_Callback(hObject, eventdata, handles)
% hObject    handle to satclose_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of satclose_text as text
%        str2double(get(hObject,'String')) returns contents of satclose_text as a double


% --- Executes during object creation, after setting all properties.
function satclose_text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to satclose_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function monopen_text_Callback(hObject, eventdata, handles)
% hObject    handle to monopen_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of monopen_text as text
%        str2double(get(hObject,'String')) returns contents of monopen_text as a double


% --- Executes during object creation, after setting all properties.
function monopen_text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to monopen_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function monclose_text_Callback(hObject, eventdata, handles)
% hObject    handle to monclose_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of monclose_text as text
%        str2double(get(hObject,'String')) returns contents of monclose_text as a double


% --- Executes during object creation, after setting all properties.
function monclose_text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to monclose_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function sunopen_text_Callback(hObject, eventdata, handles)
% hObject    handle to sunopen_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of sunopen_text as text
%        str2double(get(hObject,'String')) returns contents of sunopen_text as a double


% --- Executes during object creation, after setting all properties.
function sunopen_text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to sunopen_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function sunclose_text_Callback(hObject, eventdata, handles)
% hObject    handle to sunclose_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of sunclose_text as text
%        str2double(get(hObject,'String')) returns contents of sunclose_text as a double


% --- Executes during object creation, after setting all properties.
function sunclose_text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to sunclose_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in popupmenu1.
function popupmenu1_Callback(hObject, eventdata, handles)
% hObject    handle to popupmenu1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns popupmenu1 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupmenu1


% --- Executes during object creation, after setting all properties.
function popupmenu1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupmenu1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in randomize_button.
function randomize_button_Callback(hObject, eventdata, handles)
% hObject    handle to randomize_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

%this function figures out what today is, which shops are open, and what
%you want (ie, the preferences) -- then chooses a random shop from that
%list. the rating is used as a weighting factor, so that more awesome shops
%are chosen more frequently.
%
t = now(); %get the current time
dow = datestr(t,'ddd'); %day of week (in string format)
matdow = {'Sun','Mon','Tue','Wed','Thu','Fri','Sat'}; %matlab's ddd strings
daynames = {'sun','mon','tues','weds','thurs','fri','sat'}; %my day strings
whichday = find(strcmp(dow,matdow)); %numerical reference to which day it is
v = datevec(t);
tod = v(4) + v(5)/60; %time of day

%need open, close, coffee, tea, beer, work, social, rating
cdata = zeros(handles.nshops,8);
for j=1:handles.nshops
    cdata(j,1:2) = handles.db.shops(j).hours(:,whichday)';
    cdata(j,3) = handles.db.shops(j).hascoffee;
    cdata(j,4) = handles.db.shops(j).hastea;
    cdata(j,5) = handles.db.shops(j).hasbeer;
    cdata(j,6) = handles.db.shops(j).haswork;
    cdata(j,7) = handles.db.shops(j).hassocialize;
    cdata(j,8) = handles.db.shops(j).rating;
end

%find which shops are open... and will be for at least an hour.
isopen = (cdata(:,1)<=tod) .* (tod<=(cdata(:,2)-1));

%figure out which other preferences to care about
prefs = [get(handles.wantcoffee_checkbox,'Value'), ...
    get(handles.wanttea_checkbox,'Value'), ...
    get(handles.wantbeer_checkbox,'Value'), 0, 0]; %drinks
prefs(get(handles.wantactivity_popup,'Value')+3) = 1; %work/socialize
hasprefs = prod(cdata(:,logical([0,0,prefs,0])),2);

%which shops meet the specs
isvalid = isopen.*hasprefs;
idx = find(isvalid);

%do the randomizing
weights = cdata(idx,end);
ridx = randsample(numel(idx),1,true,weights);

%update the display
handles.databaseidx = idx(ridx);
handles = showEntry(handles, handles.databaseidx);

%save the datas
guidata(hObject, handles);



% --- Executes on button press in addasnew_button.
function addasnew_button_Callback(hObject, eventdata, handles)
% hObject    handle to addasnew_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.db.shops(handles.nshops+1) = getDisplayedInfo(handles);
handles.nshops = handles.nshops+1;
handles = populateDatabaseListing(handles); %update the database list
handles.databaseidx = handles.nshops;
set(handles.shopdatabase_popup,'Value',handles.databaseidx);
shops = handles.db.shops;
save(handles.databasefile, 'shops');
disp('Database file updated with new shop.');
guidata(hObject, handles);


% --- Executes on button press in remove_button.
function remove_button_Callback(hObject, eventdata, handles)
% hObject    handle to remove_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
killname = handles.db.shops(handles.databaseidx).name;
handles.db.shops(handles.databaseidx) = []; %remove the entry
if handles.databaseidx ~=1
    handles.databaseidx = handles.databaseidx - 1; %shift to the previous entry
end
handles.nshops = handles.nshops - 1; %decrease the shop-count
handles = populateDatabaseListing(handles); %re-up the listing
handles = showEntry(handles, handles.databaseidx);
shops = handles.db.shops;
save(handles.databasefile,'shops');
disp([killname,' has been removed from the database.']);
guidata(hObject, handles);


% --- Executes on selection change in shopdatabase_popup.
function shopdatabase_popup_Callback(hObject, eventdata, handles)
% hObject    handle to shopdatabase_popup (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns shopdatabase_popup contents as cell array
%        contents{get(hObject,'Value')} returns selected item from shopdatabase_popup
handles.databaseidx = get(hObject,'Value');
handles = showEntry(handles, handles.databaseidx);
guidata(hObject, handles);


% --- Executes during object creation, after setting all properties.
function shopdatabase_popup_CreateFcn(hObject, eventdata, handles)
% hObject    handle to shopdatabase_popup (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in wantcoffee_checkbox.
function wantcoffee_checkbox_Callback(hObject, eventdata, handles)
% hObject    handle to wantcoffee_checkbox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of wantcoffee_checkbox


% --- Executes on button press in wanttea_checkbox.
function wanttea_checkbox_Callback(hObject, eventdata, handles)
% hObject    handle to wanttea_checkbox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of wanttea_checkbox


% --- Executes on selection change in wantactivity_popup.
function wantactivity_popup_Callback(hObject, eventdata, handles)
% hObject    handle to wantactivity_popup (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns wantactivity_popup contents as cell array
%        contents{get(hObject,'Value')} returns selected item from wantactivity_popup


% --- Executes during object creation, after setting all properties.
function wantactivity_popup_CreateFcn(hObject, eventdata, handles)
% hObject    handle to wantactivity_popup (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in wantbeer_checkbox.
function wantbeer_checkbox_Callback(hObject, eventdata, handles)
% hObject    handle to wantbeer_checkbox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of wantbeer_checkbox


% --- Executes on button press in hascoffee_checkbox.
function hascoffee_checkbox_Callback(hObject, eventdata, handles)
% hObject    handle to hascoffee_checkbox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of hascoffee_checkbox


% --- Executes on button press in hastea_checkbox.
function hastea_checkbox_Callback(hObject, eventdata, handles)
% hObject    handle to hastea_checkbox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of hastea_checkbox


% --- Executes on button press in hasbeer_checkbox.
function hasbeer_checkbox_Callback(hObject, eventdata, handles)
% hObject    handle to hasbeer_checkbox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of hasbeer_checkbox


% --- Executes on button press in addmap_button.
function addmap_button_Callback(hObject, eventdata, handles)
% hObject    handle to addmap_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
disp('Add map has not been plemented yet, sorry.');


% --- Executes on button press in haswork_checkbox.
function haswork_checkbox_Callback(hObject, eventdata, handles)
% hObject    handle to haswork_checkbox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of haswork_checkbox


% --- Executes on button press in hassocialize_checkbox.
function hassocialize_checkbox_Callback(hObject, eventdata, handles)
% hObject    handle to hassocialize_checkbox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of hassocialize_checkbox


% --- Executes on selection change in rating_popup.
function rating_popup_Callback(hObject, eventdata, handles)
% hObject    handle to rating_popup (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns rating_popup contents as cell array
%        contents{get(hObject,'Value')} returns selected item from rating_popup


% --- Executes during object creation, after setting all properties.
function rating_popup_CreateFcn(hObject, eventdata, handles)
% hObject    handle to rating_popup (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


function handles = loadDatabaseFromFile(handles)
handles.db = load(handles.databasefile);
handles.nshops = numel(handles.db.shops);
handles = populateDatabaseListing(handles);


function handles = populateDatabaseListing(handles)
namedata = cell(handles.nshops,1);
for j=1:handles.nshops
    namedata{j} = handles.db.shops(j).name;
end
set(handles.shopdatabase_popup,'String',namedata);


function handles = showEntry(handles,idx)
set(handles.shopname_text,'String',handles.db.shops(idx).name);
set(handles.location_text,'String',handles.db.shops(idx).location);
set(handles.shopdatabase_popup,'Value',idx);
set(handles.hascoffee_checkbox,'Value', handles.db.shops(idx).hascoffee);
set(handles.hastea_checkbox,'Value', handles.db.shops(idx).hastea);
set(handles.hasbeer_checkbox,'Value',handles.db.shops(idx).hasbeer);
set(handles.haswork_checkbox,'Value',handles.db.shops(idx).haswork);
set(handles.hassocialize_checkbox,'Value',handles.db.shops(idx).hassocialize);
set(handles.rating_popup,'Value',5-handles.db.shops(idx).rating);
% 
% if ~isempty(handles.db.shops(idx).map)
%     set(handles.map_axes,'Visible','on');
%     set(handles.nomap_text,'Visible','off');
%     imagesc(handles.map_axes, handles.db.shops(idx).map);
%     axis image; ticksoff;
% else
%     set(handles.nomap_text,'Visible','on');
%     set(handles.map_axes,'Visible','off');
% end

daynames = {'sun','mon','tues','weds','thurs','fri','sat'};
hours = handles.db.shops(idx).hours;
for j=1:7
    if ~isnan(hours(1,j))
        set(handles.([daynames{j},'open_text']),'String',num2str(hours(1,j)));
    else
        set(handles.([daynames{j},'open_text']),'String','?');
    end
    
    if ~isnan(hours(2,j))
        set(handles.([daynames{j},'close_text']),'String',num2str(hours(2,j)));
    else
        set(handles.([daynames{j},'close_text']),'String','?');
    end
end


% --- Executes on button press in updatecurrent_button.
function updatecurrent_button_Callback(hObject, eventdata, handles)
% hObject    handle to updatecurrent_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
idx = handles.databaseidx;
namechange = ~strcmp(handles.db.shops(idx).name, get(handles.shopname_text,'String'));
handles.db.shops(idx) = getDisplayedInfo(handles); %read all the data onscreen
if namechange
    handles = populateDatabaseListing(handles); %update the pop-up list w names
end

shops = handles.db.shops;
save(handles.databasefile, 'shops');
disp('Coffeeshop database information updated.');

guidata(hObject, handles);



function S = getDisplayedInfo(handles)
S = handles.db.shops(1); %use the first entry as a template
S.name = get(handles.shopname_text,'String');

daynames = {'sun','mon','tues','weds','thurs','fri','sat'};
hours = nan(2,7);
for j=1:7
    opentime = str2double(get(handles.([daynames{j},'open_text']),'String'));
    closetime = str2double(get(handles.([daynames{j},'close_text']),'String'));
    hours(1,j) = opentime;
    hours(2,j) = closetime;
end
S.hours = hours;

S.location = get(handles.location_text,'String');
S.hascoffee = get(handles.hascoffee_checkbox,'Value');
S.hastea = get(handles.hastea_checkbox,'Value');
S.hasbeer = get(handles.hasbeer_checkbox,'Value');
S.haswork = get(handles.haswork_checkbox,'Value');
S.hassocialize = get(handles.hassocialize_checkbox,'Value');
S.rating = 5-get(handles.rating_popup,'Value');

S.map = []; %TODO: check whether a map is being shown!
