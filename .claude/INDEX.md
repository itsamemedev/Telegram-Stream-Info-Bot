# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 11016  GET              /                                                dashboard
 12505  GET              /api/abo/status                                  api_abo_status
 12486  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11633  GET              /api/automation/status                           api_automation_status
 11655  POST             /api/automation/toggle                           api_automation_toggle
 20888  GET              /api/channel/categories                          api_channel_categories
 20894  POST             /api/channel/set                                 api_channel_set
 20745  GET              /api/channels/status                             api_channels_status
 20447  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20430  GET              /api/clips                                       api_clips
 20476  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20376  GET              /api/debug/threads                               api_debug_threads
 12491  GET              /api/events                                      api_events
 12007  GET              /api/events/stream                               api_events_stream
 11870  GET              /api/health                                      api_health
 20407  POST             /api/highlights/config                           api_highlights_config
 10946  POST             /api/login                                       dashboard_login_submit
 12723  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11940  GET              /api/notify/status                               api_notify_status
 11951  POST             /api/notify/test                                 api_notify_test
 12559  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12536  GET              /api/proxy/trend                                 api_proxy_trend
 20494  GET              /api/tts/<fn>                                    api_tts_file
 21242  GET              /api/upload_window                               api_upload_window
 12109  GET              /archive/<int:eid>/download                      archive_download
 12135  GET              /download/<int:recording_id>                     download
 12068  GET              /health                                          health
 20248  GET              /healthz                                         healthz
 10937  GET              /login                                           dashboard_login_page
 10971  GET              /logout                                          dashboard_logout
 10978  GET              /manifest.webmanifest                            pwa_manifest
 21223  GET              /overlay                                         overlay_page
 11002  GET              /pwa-icon-<variant>.png                          pwa_icon
 10988  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (352)

```
   195  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   422  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
  1023  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   764  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   894  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   874  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   912  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   832  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   382  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   393  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   403  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   426  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   433  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   444  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   572  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   670  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1261  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1293  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   367  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   976  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   956  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1129  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1177  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1228  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1087  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   931  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   504  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   768  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   650  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   633  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   625  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   812  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   777  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   797  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   684  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    86  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   238  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   263  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   268  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   417  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   408  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   343  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   230  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   196  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   179  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   399  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   532  GET              /api/beobachtung/dienste                         api_beobachtung_dienste   [nc/routes/beobachtung.py]
   525  GET              /api/beobachtung/lage                            api_beobachtung_lage   [nc/routes/beobachtung.py]
   547  POST             /api/beobachtung/steuern                         api_beobachtung_steuern   [nc/routes/beobachtung.py]
   376  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   174  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    39  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    51  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   443  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   446  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   431  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   251  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   186  POST             /api/cookies/bereinigen                          api_cookies_bereinigen   [nc/routes/settings.py]
   131  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    72  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    79  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   497  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   272  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   299  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   392  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   336  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   354  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   259  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   164  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   125  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   146  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    91  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   244  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   170  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   188  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   160  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    63  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   136  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    79  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   125  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   139  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   154  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
    56  GET              /api/einstellungen                               api_einstellungen   [nc/routes/einstellungen.py]
    68  POST             /api/einstellungen                               api_einstellungen_setzen   [nc/routes/einstellungen.py]
   102  POST             /api/einstellungen/uebernehmen                   api_einstellungen_uebernehmen   [nc/routes/einstellungen.py]
    86  POST             /api/einstellungen/zuruecksetzen                 api_einstellungen_zuruecksetzen   [nc/routes/einstellungen.py]
   193  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   178  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    89  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   111  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   132  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   149  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    79  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   208  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    43  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   222  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   242  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   269  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   394  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   297  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   414  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   409  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   485  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   307  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   225  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   247  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   174  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   152  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   131  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   181  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
    66  GET              /api/lagebild                                    api_lagebild   [nc/routes/lagebild.py]
   428  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    79  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   111  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   121  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    53  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    71  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   146  GET              /api/mcp/export                                  api_mcp_export   [nc/routes/mcp.py]
    85  GET              /api/mcp/server                                  api_mcp_server_liste   [nc/routes/mcp.py]
   111  POST             /api/mcp/server                                  api_mcp_server_anlegen   [nc/routes/mcp.py]
   116  POST             /api/mcp/server/<sid>                            api_mcp_server_aendern   [nc/routes/mcp.py]
   121  DELETE           /api/mcp/server/<sid>                            api_mcp_server_loeschen   [nc/routes/mcp.py]
   132  POST             /api/mcp/server/<sid>/test                       api_mcp_server_test   [nc/routes/mcp.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   101  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    67  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    78  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   148  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   143  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   134  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    54  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    93  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   257  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   324  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   352  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   203  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   270  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   505  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   168  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   151  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   391  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   238  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   229  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   212  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
   121  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   268  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   590  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   565  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   974  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1096  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1124  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1144  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   961  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
  1023  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
  1010  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   991  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   636  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   631  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   679  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   562  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   889  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   653  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   616  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   589  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   863  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   733  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   822  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   728  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   661  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   441  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   906  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   529  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   784  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   939  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   924  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   485  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   723  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   709  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   692  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   749  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1287  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1408  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1251  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   842  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   738  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   490  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   468  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   522  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   539  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   591  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   444  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   613  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   552  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   578  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   148  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   160  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   487  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   477  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   517  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   366  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   456  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   578  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   397  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   427  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   126  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   273  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    88  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   298  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   230  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   254  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   185  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   150  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   210  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    56  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   219  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    74  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   118  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   141  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   105  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   375  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   389  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   189  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   237  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   458  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   487  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   407  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   420  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   516  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   393  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   268  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   337  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   324  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   164  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   282  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   133  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   374  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   429  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   265  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   453  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   419  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   478  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   458  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   441  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   434  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   251  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   317  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    52  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    92  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   123  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
   107  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   131  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   152  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   164  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    89  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   113  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    67  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   199  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
    73  GET              /fonts/<name>                                    schrift   [nc/routes/schriften.py]
    66  GET              /fonts/schriften.css                             schriften_css   [nc/routes/schriften.py]
   469  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (67)

```
  2231  /about                  Ueber diesen Bot
   968  /ai                     
  2231  /aireset                KI-Kontext zuruecksetzen
  1383  /ask                    
  1069  /assign_role            
  1119  /ban                    
  2187  /botstats               
  2231  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2231  /bulkadd                Mehrere User auf einmal tracken · a b c
  2231  /cleanup                Alte Aufnahmen aufraeumen
  1649  /clearwarns             
  2151  /clip                   
  2136  /clipoftheweek          
  1519  /clips                  
  2231  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
  1024  /create_category        
   995  /create_channel         
  1059  /create_group           
  1034  /create_role            
  1010  /create_voice           
  1260  /daily                  
  2231  /diag                   Vollstaendige Diagnose
  2231  /einnahmen              Einnahmen und Spenden
  1412  /event                  
  1454  /events                 
  1559  /follow                 
  1548  /help                   
  1109  /kick                   
  1232  /leaderboard            
  2231  /live                   Live-Status sofort pruefen · @user
  1506  /livenow                
  2231  /logs                   Letzte Fehler aus dem Log
  2231  /pause                  Tracking pausieren · @user
  1534  /post_test              
  1344  /profile                
  1141  /purge                  
  2231  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2231  /quota                  Speicher-Quota
  1219  /rank                   
  1494  /recstatus              
  1079  /remove_role            
  2231  /report                 Azrael-Sentinel-Wochenreport
   981  /restream_status        
  2231  /resume                 Tracking fortsetzen · @user
  1089  /set_channel_perms      
  1181  /setup_community        
  1198  /setup_targets          
  1480  /spenden                
  1591  /stats                  
   940  /status                 
  2231  /stoprec                Laufende Aufnahme sauber beenden · @user
  1687  /streaminfo             
  2231  /summary                Tageszusammenfassung
  2231  /sysres                 System-Ressourcen
  2231  /teststream             Recorder-Selbsttest · @user
  2231  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1129  /timeout                
  1659  /topstreamers           
  2231  /topusers               Top-Streamer nach Aufnahmen
   870  /track                  
  2231  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   953  /tracklist              
  1573  /unfollow               
  2231  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   902  /untrack                
  1612  /warn                   
  1635  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2398  on_member_join
  2355  on_message
  2252  on_raw_reaction_add
  2433  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    60-75     konfiguriere
    78-533    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (53 Funktionen)

```
  1764-1815   _award_xp
   537-564    _bereich_umziehen
   484-494    _clip_kopieren
  1986-2015   _clip_week_leader
  2039-2053   _clipoftheweek_loop
  2550-2612   _community_events_loop
  1721-1743   _dc_client
  1746-1755   _dc_offen
  2652-2687   _disc_automod_check
   410-415    _disc_sprache_setzen
  1818-1866   _discord_ai_automod
   673-712    _discord_automod
  1869-1889   _discord_azrael_reply
  2056-2509   _discord_run_once
   245-303    _discord_start
   306-360    _ensure_discord_invite
  2515-2547   _ensure_error_channel
   431-444    _ensure_rank_roles
   833-847    _ensure_team_roles
  2615-2645   _error_channel_loop
   722-726    _guard
   642-670    _handle_voice_ai
   418-428    _is_admin
   509-534    _link_video
  1934-1945   _liveboard_loop
   729-762    _on_level_up
   638-639    _par_chat_id
  2018-2036   _post_clip_of_week
  1948-1966   _post_weekly_digest
   447-473    _provision_base_channels
  1486-1580   _reg_betrieb
  1155-1249   _reg_community_setup
  1252-1333   _reg_daily_profil
  1376-1473   _reg_frage_events
   927-983    _reg_info
  1101-1152   _reg_moderation
  1336-1373   _reg_profil
  1050-1098   _reg_rollen
   986-1047   _reg_server
  1476-1483   _reg_spenden
  1583-1670   _reg_streamer
  1673-1718   _reg_system
   861-924    _reg_tracking
   797-830    _run_tg_handler
   162-224    _uebernehmen
   497-506    _umzugsmarken
  1898-1931   _update_liveboard
  1969-1983   _weekly_digest_loop
   476-481    _ziel_guild
   567-609    _ziele_abgleichen
   618-635    _ziele_sync_loop
   612-615    _ziele_takt_min
   227-230    starte
```

## Top-Level-Symbole in bot.py (576 Funktionen, 4 Klassen)

```
 25982-26004  _abbruch_datenbank_unlesbar
  2816-2817   _abo_key
  2837-2855   _abo_probe_dump
 26104-26120  _abschied_wachen
 26123-26141  _abschluss
 16498-16505  _ad_allowlist
 17664-17670  _agent_for
 17673-17689  _ai_telemetry
 18205-18223  _alert
 21660-21710  _alert_monitor_loop
 18910-18967  _alte_beilagen_einsammeln
 22091-22153  _announce_loop
  3767-3777   _anthropic_key
  3780-3782   _anthropic_model
 10505-10508  _arg_int
  2808-2813   _as_dict
 25668-25677  _async_exc_handler
 18394-18416  _audio_tap_cmd
 19434-19493  _audio_tap_melden
 18430-18454  _audio_tap_sammler
  9854-9891   _aufnahme_beim_stopp_sichern
 18852-18873  _aufnahme_chat_ausklang
 18836-18849  _aufnahme_chat_beginnen
 18995-19016  _aufnahme_chat_dienst
 19194-19247  _aufnahme_chat_einarbeiten
 18831-18833  _aufnahme_chat_modus
 19019-19068  _aufnahme_chat_nachtrag
 18876-18907  _aufnahme_chat_vormerken
 18986-18992  _aufnahme_chat_wecken
 24793-24795  _aufnahme_deckel
 19071-19092  _aufnahme_fertigmachen
 22328-22381  _aufnahme_nach_discord
  9894-9912   _aufnahme_platz_frei
  9797-9824   _aufnahme_verteilen
 26068-26088  _aufnahmen_abschliessen
 26007-26065  _aufraeumen
 10779-10848  _auth_cookie
 10735-10775  _auth_guard
  2063-2068   _auto_on
 20119-20137  _auto_restream_loop
 13973-14015  _avatar_frames_laden
 16548-16561  _azrael_brain_kontext
 23285-23300  _azrael_broadcast_reply
 23185-23207  _azrael_chat_reply
 23157-23182  _azrael_chat_should_reply
 23213-23215  _azrael_gate_cfg
  4219-4232   _azrael_ki
 17692-17706  _azrael_live_state
  4235-4257   _azrael_lokal
 21138-21152  _azrael_overlay_state
 17748-17756  _azrael_persona_kern
 18087-18141  _azrael_proactive_loop
 17512-17568  _azrael_reaction_to_chats
 23218-23225  _azrael_reply_all_chats
  4260-4275   _azrael_schweigt_melden
 23144-23154  _azrael_self_names
 23253-23282  _azrael_send_to
 13934-13970  _azrael_spricht
 14281-14294  _azrael_stimme_stumm
 17712-17745  _azrael_system
 21794-21797  _backup_active
 21875-21888  _backup_loop
  5408-5431   _betreiber_pruefen
 24882-24886  _betrieb
 25741-25750  _brain_crowdsec_snap
 25909-25912  _brain_db_health
 21581-21590  _brain_growth_loop
 11145-11172  _brain_growth_snapshot
  2727-2761   _brain_hint_delay
 25813-25848  _brain_moderation_snap
  6692-6720   _brain_notify
 25915-25937  _brain_recording_snap
 25753-25810  _brain_restream_health
 25940-25953  _brain_tiktok_status_snap
 11986-12003  _browser_push
 14328-14332  _build_restream_cmd
  5434-5461   _can_stop_tracking
  2174-2196   _capture_set_cookies
 12589-12592  _cfg_get
 12595-12597  _cfg_set
 20849-20884  _channel_set_all
 13032-13035  _chat_connected
 13038-13054  _chat_disconnected
 18980-18983  _chat_einarbeiten_async
  9288-9318   _chat_is_forum
 18800-18825  _chat_listener_abbauen
  9460-9495   _chat_migriert
  9498-9499   _chat_migriert_async
 13068-13070  _chat_sanitize
 13017-13029  _chat_stat
  4094-4106   _check_ai_models_sync
 11340-11383  _classify_pool_anonymity
   916-938    _claude_chat_sync_metered
 10537-10543  _client_ip
 22786-22800  _clip_chat_ass
 22237-22271  _clip_prune
 22274-22284  _clip_recfile_for
 22706-22774  _clip_schneiden
 22803-22809  _clip_should_velocity
 22384-22469  _clip_to_discord
 19165-19170  _clips_abwarten
  3967-3976   _close_ai_session
 23331-23346  _cohost_broadcast
 23316-23317  _cohost_cfg
 23372-23384  _cohost_fire_highlight
 23320-23328  _cohost_gate
 23349-23369  _cohost_highlight
  7022-7083   _cookie_alarm_loop
  2264-2265   _cookie_autofetch_info
  2248-2252   _cookie_autorefresh_info
 25343-25365  _cookie_bezug_loop
 25368-25393  _cookie_bezug_runde
  2151-2155   _cookie_header
 10546-10551  _cookie_sicher
  2277-2291   _cookies_selbst_holen
  4365-4367   _create_index_safe
  6908-6935   _daily_summary_loop
  3293-3318   _darf_ytdlp_nachschlagen
 12150-12171  _dashboard_adresse
 10566-10570  _dashboard_hostnamen
  1516-1546   _dashboard_trackings_umziehen
 22777-22783  _datei_weg
 21634-21657  _db_maintenance_loop
  6858-6905   _db_vacuum_loop
 16521-16545  _detect_foreign_ad
  1744-1755   _diag_path_owner
 17992-18037  _director_finalize
 19424-19431  _director_for
 17941-17989  _director_mark
 22619-22622  _disc_state_get
 22625-22632  _disc_state_set
 21562-21571  _discord_bot_starten
 21525-21536  _discord_einladung_merken
 21574-21578  _discord_invite
 21539-21559  _discord_kontext
 22580-22616  _discord_live_thread
 18144-18156  _discord_notify
 21497-21522  _discord_ops_alert
 22480-22576  _discord_post_user
 22156-22162  _discord_stop
  6938-7019   _disk_alarm_loop
 25214-25265  _disk_autoclean
 25524-25537  _disk_guard_loop
 13913-13920  _drossel_hoeher
 13909-13910  _drossel_stufe
 13923-13931  _drossel_zuruecksetzen
 12327-12329  _dump_all_threads
 24889-24903  _einstellungen_startzeile
  2316-2377   _ensure_cookie_file_netscape
  9389-9392   _ensure_notify_topic
 11490-11527  _ensure_proxy_ready
  9328-9351   _ensure_topic
   759-761    _env_int
   764-766    _env_int_range
 18189-18202  _event_webhook
 12815-12828  _evolution_loop
  6123-6157   _extract_file_payload
  1502-1513   _fanout_ziele
 26144-26207  _fatal_vom_botteil
 24798-24813  _fd_grenze_anheben
  5003-5013   _fehler_text
 11239-11257  _fetch_proxy_list
 18769-18797  _fetch_tiktok_room_id
   844-847    _ff_cmd
 19178-19191  _ffprobe_masse
 13857-13873  _fifo_schreiber_wecken
 13667-13672  _find_chromium
  3688-3690   _find_external_recorder
  2440-2442   _find_stream_urls
 12638-12663  _fire_webhooks
  7952-7962   _fork_safe
   949-962    _freeai_chat_sync_metered
  3955-3964   _get_ai_session
  7780-7820   _get_live_info
  3137-3144   _get_resolve_semaphore
  8477-8898   _handle_single_tracking
 24998-25000  _hb
 25003-25020  _hb_while
 20361-20372  _healthz_fuer_aufrufer
 25044-25072  _heap_zurueckgeben
 10852-10869  _herkunft_guard
 13082-13084  _highlight_cfg
 13087-13116  _highlight_observe
 13718-13726  _htmlov_bild_schreiben
 13696-13715  _htmlov_dauerbrowser
 13675-13693  _htmlov_screenshot_cmd
 18456-18466  _httpx_proxy
 12671-12683  _in_quiet_hours
 25968-25979  _init_db_oder_abbruch
 26821-26852  _install_fast_eventloop
 10400-10454  _install_fast_json
 12332-12348  _install_faulthandler
 20157-20166  _intel_ensure_schema
 20209-20244  _intel_index_loop
 20178-20193  _intel_index_one
 20169-20175  _intel_semantic
  5393-5406   _is_authorized
  8303-8324   _is_dead
  1963-1970   _is_process_running
  6722-6729   _is_quiet_hours
  1404-1413   _is_upload_window
  4868-4883   _iso
 10554-10563  _ist_lokal
 10489-10502  _json_error_handler
  4024-4033   _ki_rueckfall_melden
  8178-8185   _kick_cluster_gefunden
  8113-8175   _kick_cluster_weiter
  6771-6813   _kick_follower_count
  6755-6758   _kick_slug
  8083-8110   _kick_ws_pause
 25956-25965  _kickmod_boot
 25309-25312  _lagebild_discord_aufnahme
 25322-25326  _lagebild_kick_chat
 25315-25319  _lagebild_overlay
 25329-25331  _lagebild_spendenziel
 25296-25306  _lagebild_upload
 12700-12702  _latest_popularity
  1900-1909   _laufstand
 25484-25521  _laufstand_loop
 24922-24960  _leistung_erheben
  7669-7696   _link_video_senden
  8464-8475   _live_check_frist_melden
  2871-2884   _live_ohne_stream
 19829-19878  _live_react_loop
 19496-19818  _live_react_worker
  3536-3650   _live_status_aufloesen
 17571-17582  _live_transcript_push
 19820-19827  _live_users
 18040-18084  _living_title_loop
 21800-21872  _local_backup_scan
  4808-4831   _lock_update
 10471-10485  _log_5xx
 24963-24995  _log_schleuse_pruefen
   834-841    _log_sicher
 14340-14352  _looks_like_codec_err
 14335-14337  _looks_like_source_expired
  8001-8031   _loop_fehler
 12351-12360  _loop_heartbeat
 24704-24737  _loop_lag_monitor
 24751-24771  _loop_stockung_melden
 24774-24784  _loop_takt_starten
 12363-12436  _loop_watchdog_thread
 17448-17465  _loyalty_add
 17439-17445  _loyalty_get
 17468-17476  _loyalty_top
  5114-5133   _manual_status
  8326-8327   _mark_dead
 11710-11726  _marketing_loop
 23232-23250  _maybe_handle_command
 25623-25647  _maybe_hype_clip
 22206-22234  _meme_klassifizieren
 19095-19162  _meme_zusammenschnitt
  4352-4357   _migrate_columns
 23514-23525  _mod_is_exempt
 23528-23533  _mod_warn_first
 23536-23539  _mod_warn_text
 12857-12876  _modlog
 12840-12854  _modlog_schreiben
  1100-1102   _multistream_targets
  3321-3357   _nachschlag_ytdlp
  7965-7966   _nc_create_subprocess_exec
  7969-7970   _nc_create_subprocess_shell
 11824-11841  _news_loop
 12899-12901  _normalize_ingest
  2658-2675   _note_check_duration
  9383-9386   _notify_topic_name
  2862-2868   _offline_ergebnis
  3360-3383   _ohne_url_melden
 17597-17605  _oracle_memories
 17892-17926  _oracle_memorize
 17608-17621  _oracle_persona
 17590-17594  _oracle_recent_text
 13291-13292  _ov_atomic_write
 13282-13284  _ov_bar
 16426-16438  _ov_clip_text
 13287-13288  _ov_oneline
 21187-21216  _overlay_push
 13621-13664  _overlay_render_size
 12968-12972  _overlay_session_reset
 21154-21156  _overlay_src_ok
 13301-13313  _overlay_takt
 16508-16518  _own_invites
 13616-13618  _parse_size
  7333-7366   _pause_resume_cmd
  2202-2246   _persist_refreshed_cookies
  2105-2137   _pick_checked_pull_proxy
 10620-10635  _pin_auth_value
 10724-10725  _pin_clear_fail
 10688-10691  _pin_global_gesperrt
 10641-10652  _pin_hmac_schluessel
 10694-10701  _pin_locked
 10704-10721  _pin_note_fail
 10655-10676  _pin_ok
 20982-21007  _piper_pick_model
 21067-21132  _piper_say
 12600-12635  _post_json_threaded
 13595-13613  _probe_video_size
  1991-2008   _proc_is_recorder
 11459-11487  _proxy_pool_refresh_loop
  2071-2102   _proxy_report_recording
  9037-9118   _pruef_runde
  8996-9034   _pruefstand_melden
 24833-24844  _pruefung_verworfen
 12317-12319  _prune_stall_dumps
  2268-2274   _pull_proxy_still
 18160-18186  _push_notify
 10916-10918  _pwa_dir
 11308-11325  _quick_validate_proxy
 12666-12668  _quiet_hours_config
 10881-10914  _rate_guard
  2887-2915   _raumsperre_fragen
 17409-17415  _react_warn
  7867-7906   _reap_proc
 10573-10589  _rebinding_melden
  9727-9794   _rec_auto_abschalten
  9674-9724   _rec_frueh_getrennt
  9539-9619   _rec_kategorie_melden
  9622-9671   _rec_totstreak_fortschreiben
  2698-2720   _record_check_outcome
   829-831    _redact_stream_urls
 11386-11456  _refresh_proxy_pool
  2475-2566   _resolve_via_html
  2918-3114   _resolve_via_webcast_api_v2
  3182-3269   _resolve_via_ytdlp
 22843-22972  _resolve_youtube_ingest
  2451-2472   _resolver_stumm
 12951-12962  _restream_active_sources
 14018-14145  _restream_avatar_feeder_start
 14148-14158  _restream_avatar_feeder_stop
 19250-19388  _restream_chat_guardian
 13119-13191  _restream_chat_push
 13268-13277  _restream_chat_push_async
 25851-25906  _restream_durchreicher
 13729-13854  _restream_html_overlay_start
 13876-13896  _restream_html_overlay_stop
 12910-12933  _restream_overlay_files
 19881-19913  _restream_platform_state
 20081-20116  _restream_resume_after_restart
 13222-13239  _restream_soll_schreiben
 13242-13265  _restream_status_schreiben
 14206-14278  _restream_tts_enqueue_wav
 13557-13589  _restream_tts_feeder
 13554-13555  _restream_tts_fifo_path
 14161-14188  _restream_tts_start
 14190-14204  _restream_tts_stop
 19919-20078  _restream_verify_loop
 21765-21777  _retention_loop
 21759-21762  _retention_scan
  2819-2821   _room_is_abo
  6160-6288   _run_ai_call
 12459-12472  _run_async_from_flask
 26810-26818  _run_selfcheck_and_exit
 21780-21791  _s3_client
  8353-8423   _safe_send
  5077-5093   _sample_net_throughput
 26790-26807  _sc_bericht
 26731-26787  _sc_dienste
 26638-26728  _sc_ki_und_stimme
 26589-26635  _sc_umgebung
  2764-2794   _schedule_next_check
 21713-21756  _scheduler_loop
  4360-4362   _schema_pk
 12475-12480  _scraper_session
 23542-23581  _screen_full
 11886-11923  _sec_headers
  2435-2437   _select_stream_from_data_section
 26499-26586  _selfcheck
  9395-9429   _send_live_notice
  1427-1431   _should_defer_upload
 22287-22325  _shrink_for_discord
 10921-10933  _sicheres_ziel
 21593-21631  _sicherheits_erinnerung_loop
 25544-25561  _sign_health_check
 25564-25583  _sign_health_loop
  4886-4911   _sitzung_bestimmen
 20344-20354  _sparen_lage
  7982-7993   _spawn
 27240-27270  _spawn_from_flask
 24847-24853  _speicher_maps
 24856-24871  _speicher_pflegen
 18468-18766  _start_chat_listener
 24816-24830  _start_gesperrt
 12439-12456  _start_loop_watchdog
 11772-11821  _stats_loop
 11751-11754  _stats_output_path
 11757-11769  _stats_write
 21019-21033  _stimme_saubern
 21040-21064  _stimme_schon_gesagt
  8977-8993   _storage_cleanup_loop
 25603-25610  _story_for
  3712-3718   _stream_url_expiry
  3720-3725   _stream_url_ttl
 16471-16478  _streamer_persona_get
 21897-22049  _system_backup
 22058-22088  _system_backup_loop
 12277-12295  _task_auf_bot_schleife
 24379-24395  _telegram_befehlsmenue
  8034-8080   _telegram_polling_fehler
  1472-1499   _telegram_ziele
 11260-11299  _test_proxy
 11682-11698  _testpush_resolve_live
 19173-19175  _text_schreiben
  7613-7644   _tg_ki_dialog
  9447-9457   _tg_migriert_laden
  9443-9444   _tg_migriert_pfad
  8329-8350   _tg_sprache_setzen
  9257-9267   _tg_topics_load_into_mem
  9254-9255   _tg_topics_path
  9269-9276   _tg_topics_save
 10592-10602  _token_ok
  9354-9370   _topic_anlegen
  9279-9286   _topic_forget
 12686-12697  _tracking_max_duration
  4622-4636   _tracking_remove_cleanup
  4653-4665   _tracking_resume_cleanup
  1802-1825   _try_attach_file_handler
 21009-21017  _tts_cleanup
 25268-25288  _tunnel_lage
 25429-25481  _tunnel_wacht_loop
 20512-20565  _twitch_channel_status
 23584-23732  _twitch_chat_loop
 22638-22651  _twitch_clip_versuchen
 23395-23501  _twitch_eventsub_loop
  1592-1627   _upload_queue_abarbeiten
  1450-1470   _upload_queue_add
  1563-1565   _upload_queue_count
  1433-1442   _upload_queue_load
  1630-1652   _upload_queue_nachher
  1423-1425   _upload_queue_path
  1549-1553   _upload_queue_remove
  1444-1448   _upload_queue_save
  1556-1561   _upload_queue_update
  9827-9851   _upload_rest_sichern
  1567-1589   _upload_window_loop
  7840-7847   _uptime_s
 12887-12896  _url_host
  3386-3484   _url_nachschlag
   909-913    _usage_record_claude
 25716-25738  _v37_pause_source
 25680-25690  _v37_restream_restart
 25693-25713  _v37_unpause_source
  8252-8296   _verbindung_verloren
  6816-6847   _viewer_sample_loop
 10728-10731  _wants_html
  7850-7864   _warn_empty_env
 25075-25200  _watchdog_loop
 23116-23124  _wchat_thank_ok
 25396-25426  _werkzeug_wacht_loop
 18228-18266  _whisper_get_model
  7941-7949   _whisper_native_section
 17396-17402  _whisper_pool
 18360-18392  _whisper_segments
 18268-18284  _whisper_stumm
 18287-18357  _whisper_transcribe
 13354-13511  _write_restream_overlay
 13316-13351  _write_restream_overlay_async
 23756-23855  _youtube_api_chat_loop
 20568-20671  _youtube_api_status
 20674-20741  _youtube_channel_status
 23858-24022  _youtube_chat_loop
 22654-22679  _youtube_clip_versuchen
 22978-22991  _youtube_restream_autoconfig
 22994-23018  _youtube_restream_autoconfig_inner
 23085-23113  _youtube_send
 20805-20846  _youtube_set_channel
 23021-23055  _yt_access_token
 23058-23073  _yt_live_chat_id
 23081-23082  _yt_sendrate_cfg
 23735-23750  _yt_timeout
  3161-3162   _ytdlp_detect_available
  3177-3179   _ytdlp_einzeln
  3164-3175   _ytdlp_note_result
 12322-12324  _zombie_child_count
 24906-24919  _zustand_kennzahlen
  7716-7740   about
  4541-4545   add_ai_log_entry
  4914-4985   add_recording
  4597-4614   add_tracking
  6291-6324   ai
  4115-4210   ai_chat
  4307-4317   ai_history_append
  4319-4324   ai_history_clear
  4296-4305   ai_history_load
  4281-4294   ai_rate_limit_check
  6353-6361   aireset
 17759-17778  azrael_chat
 24027-24149  brain_cmd
  3728-3733   build_recording_cmd
  4617-4620   bulk_add_trackings
  7086-7145   bulkadd
  9121-9237   check_all_trackings
  4668-4680   claim_live_transition
 16564-17328  class KickModerator
 14355-16314  class RestreamManager
  4834-4835   class _AufnahmeLockVerloren
  8188-8249   class _KickClusterSuche
 11570-11612  classify_proxy_anonymity
  6399-6598   cleanup
  5334-5340   cleanup_old_recordings
  4859-4866   clear_recording
 22682-22703  clip_moment
  7208-7284   cookies_cmd
  7287-7330   cookies_datei_cmd
  4588-4594   count_trackings_for_chat
  4528-4539   decide_preferred_recorder
  5818-5965   diag
 24261-24322  einnahmen_cmd
  4489-4505   finish_recording_attempt
  4641-4643   get_all_active_trackings
  4987-4990   get_all_recordings
  4467-4470   get_archive_entry
  2308-2313   get_cookie_health
  5057-5063   get_event_log
  4512-4526   get_last_recording_attempt
  3487-3529   get_live_status
  5068-5071   get_priority_poll_interval
  4507-4510   get_recent_recording_attempts
  4992-4995   get_recording_by_id
  3895-3924   get_redis
  5328-5332   get_storage_stats
  5107-5109   get_tiktok_status_distribution
  4682-4691   get_tracking_state
  4638-4639   get_trackings_for_group
  9915-10382  handle_recording_finished
 24371-24376  hilfe_cmd
  4375-4440   init_db
  5603-5641   live
  8426-8456   live_check_worker
  3979-4021   llm_chat
  4054-4086   llm_chat_sync
  4039-4051   llm_list_models
  5016-5049   log_event
  1925-1958   log_recording_failure
  7480-7529   logs_cmd
 26210-26489  main
  6327-6350   on_ai_media
  7606-7610   on_ai_reply
  7699-7713   on_azrael_mention
  7745-7775   on_callback
  9502-9520   on_chat_migration
  7653-7666   on_link_video
 17784-17889  oracle_handle
  7369-7372   pause_tracking
  5383-5388   profile_keyboard
  5556-5600   quelle
  7431-7477   quota
  8900-8974   reaper_loop
  5103-5105   record_tiktok_status
  6366-6396   recstatus
  3926-3934   redis_get_json
  3937-3943   redis_set_json
 24398-24408  report_cmd
 11615-11617  report_proxy_result
  2569-2611   resolve_tiktok_live_stream
  7375-7378   resume_tracking
 24411-24684  run_bot
 12174-12268  run_flask
  4548-4554   save_tiktok_check
  4838-4857   set_recording_file
  4646-4650   set_tracking_paused
 24356-24368  spenden_cmd
  9526-9537   split_and_send_video
  5466-5508   start
  4473-4487   start_recording_attempt
  6601-6639   stats
  5252-5305   stop_manual_recording
  7381-7428   stoprec
  6740-6748   summary_cmd
  7532-7603   sysres
  5967-6111   teststream
  5510-5551   tiktok
  7148-7205   topusers
  5678-5735   track
  5643-5675   track_exact
  5749-5816   tracklist
  5136-5250   trigger_manual_recording
  4770-4805   try_acquire_recording_lock
 24325-24353  unpause_cmd
  5737-5747   untrack
 24152-24258  update_cmd
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
abwehrlage.py          auswerten, configure, crowdsec_status, crowdsec_via_lapi, cscli_bin, cscli_path, darf_journal_lesen, ssh_angriffe, sudo_hinweis
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, run_archive_file_check, uebernehmen
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            aus_bestand, config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmechat.py        ass, ausschnitt, beenden, beginnen, clip_beginnt, clip_fertig, clip_merken, clips_nehmen, clips_offen, concat_liste, einbrennen_cmd, laeuft, modus, notieren, untertitel_cmd, zusammenschnitt_cmd
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest, stall_grenze
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, angleich_cmd, braucht_angleich, concat_cmd, concat_liste, gehoert_dazu, luecken, probe_cmd, sekunden, sitzung_id, tonformat, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelkontext.py       ausfall, block, fakten, letzte_erinnerung, nachricht, restream_quellen, sicher, streamer_waehlen
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_zugang, sys_backup, sys_hour, sys_keep
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
befehle.py             beschreibung, discord_nativ, discord_ueber_tg, fuer, hilfe_text, pruefen, telegram_handler
beobachtungsdienst.py  fuer_deck, grafana_jetzt, grafana_lage, grafana_unit, grund_text, installiert, prometheus_jetzt, prometheus_lage, selbstheilung_erlaubt, steuern
beobachtungslage.py    grafana, lage, prometheus
betriebslage.py        abschiedswache, bereit, bewerten, haengende_threads, sichern_beim_stopp
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            aendern, class FalscheForm, get, lesen, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatnachtrag.py        beilage_lesen, beilage_zu, eingearbeitet, ensure_schema, erledigt, fehlversuch, ist_beilage, lesen, offene, stempel, unveraendert, vormerken
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
clientip.py            echte_ip, host_ist_lokal, ist_https, ist_lokal
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
cookieholen.py         aktualisiere, aus_browser, bereinigen, class DateiGeaendert, class KeinDesktop, configure, desktop_pruefen, hole_gastcookies, schreibe, uebernehmen, zusammenfuehren
cookies.py             abgelaufen, auswahl, configure, gesundheit, hat_login, kritisch, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, gesetzte, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbgesundheit.py        messen
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwartung.py           faellig_in, letzter_lauf, merken, stand_datei
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, mariadb_lage, set_pool, treiber_fehler, treiber_wunsch, vorrat_groesse, vorrat_lage, vorrat_leeren
dcspar.py              anzeige, client_optionen, puffer
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordaufnahme.py     an, beschriftung, hochladen, teilen
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
discordziele.py        clip_kanal, clip_kanal_des_bereichs, clip_kanal_holen, eigene_kanaele, loeschbar, umzugsmarke, umzugsmarke_lesen
donations.py           configure, fmt_eur, kurse_aus_env, parse_number, summe_eur, to_eur, unknown_count, zeile_eur
donationsdb.py         manual_rows, manual_total, parse_eur
durchreicher.py        adresse, ist, main, nutzer_aus, werkzeug, werkzeuge, zieher_cmd, zieher_umgebung, zubringer_cmd
einstellungen.py       bekannt, class Abgelehnt, db_werte, geheim, gueltiger_name, in_umgebung_laden, katalog, pruefen, schutzgrund, setzen, startbericht, uebernehmen, uebersicht, zuruecksetzen
encodeschlange.py      lage, last_frei, parallel, platz, platz_sync
envdatei.py            class EnvdateiFehler, lesen, main, setzen, wert_lesen, wert_schreiben
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, schnappschuesse, schnappschuesse_kappen, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      anzeige_groesse, avatar_kette, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
forkriegel.py          class Vortritt
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
gegendruck.py          abgewiesen, deckel_auto, fd_grenze_anheben, fd_lage, freigeben, lage, reservieren, reserviert, start_entscheiden, verworfen, zuruecksetzen
geocache.py            anreichern, get, groesse, leeren, put
geoip.py               ist_privat, lookup
geschuetzt.py          lage, ruhend, vermerken, verschlossen, zuruecksetzen
heapzaum.py            arenen_wunsch, deckeln, lage, rss_mb, takt_min, zurueckgeben
herkunft.py            entscheiden
highlights.py          check, new_state, observe, score, zustand
httpsitzung.py         schliessen, sitzung, teilen
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kennzahlen.py          einwertig, prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, state_gueltig, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, class PusherGeschlossen, configure, naechster_cluster, naechster_key, oauth_exchange, pusher_fehler, pusher_lage, pusher_pause, pusher_url, schliessgrund, search_category, send_message, slug, timeout_user, update_channel, user_token
kickzentrifugo.py      als_frame, antwort_fehler, class KickZentrifugoFehler, connect_cmd, fehler_code, ist_ping, kanal, lage, neue_client_id, neues_token, pause, refresh_cmd, subscribe_cmd, token_aus, ttl_aus, verbindung_body, ws_url_aus, zerlegen, zugang
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              azrael_lage, azrael_wahl, backend, gesamtzeit, llm_zeiten, lokal_installiert, lokal_stand, lokal_zuerst, lokales_modell, normal, provider, vorrang, wartezeit, weg_zaehlen, zeitlimit
lagebild.py            bauen, dienst_quelle, dienste, dienste_lesen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
linkvideo.py           abklingzeit_s, an, aufraeumen, ausgabe_lesen, befehl, bildunterschrift, configure, darf, grund, holen, ist_tiktok, links, max_dauer_s, sperre, werkzeug
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, setzen, statistik, zaehle, zaehler_zuruecksetzen
livefolge.py           beste_url, braucht_url_nachschlag, hat_stream_url, last_dehnung, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
livemeldung.py         live_an, live_aus
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, einreihen, entkoppeln, nachziehen, schwaerzen, stoppen, synchrone_handler, verloren, wartend, zuruecksetzen
looplag.py             bremser, erfassen, lage, spaeher_starten, stelle_aus_rahmen, takt, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
mariadbumzug.py        class UmzugAbgebrochen, env_setzen, geoeffnet_von, in_benutzung, quelle_zaehlen, umziehen, vergleichen, ziel_zaehlen
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
mcpdienste.py          class Abgelehnt, class BestandUnbekannt, class Unbekannt, export, lage, liste, llama_adresse, loeschen, speichern, testen, webui
meldetakt.py           erfolg, gestoert, melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
oeffentlichestats.py   configure, public_stats
outcomes.py            get_outcome_breakdown
overlaybrowser.py      browser_cmd, class Dauerbrowser, class OverlayBrowserFehler, lage, teilen
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
piperarbeiter.py       main
piperdienst.py         an, beenden, lage, sprechen
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
profildetail.py        datum, felder, kennzahlen, kontotyp, verlauf
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
prueflage.py           fuer_healthz, lage, merken, runde_gelaufen, uebersicht, vergessen
pruefschlange.py       erledigt, mit_frist, vorgemerkt, vormerken, zuruecksetzen
qrsvg.py               qr_svg
quellprobe.py          empfehlung, form, kurz, main, maske, messen, probe_durchreicher, probe_ffprobe, probe_html, probe_ytdlp, ttl
quellstat.py           lage, zaehlen, zuruecksetzen
raumkennung.py         grund, gueltig
raumsperre.py          deuten, faellig, lage, merken, snapshot, text, vergessen
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, quelle_lage, quelle_laut, text
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, ein_start_je_ziel, fenstergroesse, freigeben, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, startend, url_host
restreamcfg.py         active_platforms, aktiv, bruecke, bruecke_luecke, bruecke_offline, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, fueller, quell_eingang, schriftart, zubringer
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              anlegen, create_schema, index_sicher, kollation_angleichen, modultabellen, parameter, spalten_nachziehen
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendebruecke.py        ausnahme_text, class Bruecke, class TsUmschreiber, ist_keyframe, pat_pmt_pid, pes_zeit, pid, pmt_stroeme, pmt_urteil, video_pid, weiche_grund
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          sicher_join, sicherer_name, unter
sicherungspruefung.py  archiv_lesbar, dump_vollstaendig, pruefen
sitzungsschluessel.py  laden, pin_schluessel
speicherpflege.py      abgelaufene_weg, alte_stempel_weg, groessen
spendeninfo.py         krypto, paypal, paypal_url, stand, text
spendenziel.py         eingang, fenster_start, ist_monatlich, stand, summe, zeitraum, ziel_eur
sqldialekt.py          bei_konflikt
sqlguard.py            abbruch_nach, check_readonly, frist_ueberschritten, frist_unbekannt, mariadb_mit_frist, normalize, with_limit
sqlutil.py             zeitfenster_literal
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             class BestandUnbekannt, cleanup, forecast, notfall_raeumen, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
tagesbericht.py        bauen, configure
telegramfehler.py      dashboard_umzug, dauer_text, ersatz, grund, ist_fehler, ist_telegram_chat, migration_plan, migriert_erlaubt, nur_telegram, standardgruppe, text, zuruecksetzen
textmore.py            configure_banned_cap, pre_nachrichten, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tgantwort.py           angesprochen, echte_antwort, entscheiden, frage_ohne_namen, gemerkt, ist_ki_antwort, merken, ohne_fuss
tgmarkdown.py          html_zu_md, teilen
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, garantie, garantie_cmd, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             ausfuehrbar_im_archiv, build_plan, check, class Plan, class UpdaterConfig, commit_zip_url, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, rechte_angleichen, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
uploadschlange.py      angekommen, faellig, gleicher, nach_versuch, pause_s
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
werkzeugpfad.py        alter_tage, befund, lage, nachahmen_aus, pruefen, voranstellen
whispercfg.py          bedarf_mb, benutzt, entladen_wenn_leer, frei_mb, gebrauch, geladen, leerlauf_s, name, rss_hinweis, verfuegbar, waehle, wechsel_pruefen
youtube_api.py         active_broadcast_params, ban_payload, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlparbeiter.py       main
ytdlpdienst.py         alle_beenden, anzahl, ausfuehren, laeufe_max, lage
ytdlpurl.py            nur_frische, urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
zeitglaetter.py        ausdruck, bsf_args, filter_text, verfuegbar
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DatabaseAgent, class DiskAgent, class GrafanaAgent, class HealthAgent, class LearningAgent, class PrometheusAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime, ohne_denkblock
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler, frische_intervalle
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
