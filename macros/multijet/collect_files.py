import eostools

if __name__ == '__main__':

    topdir = "/store/user/salvati/Razor/MultiJetAnalysis/T2tt"
    root_files = eostools.ls(topdir)
    print root_files

    import pickle
    pickle.dump(root_files, file('root_files.pkl', 'wb'))
