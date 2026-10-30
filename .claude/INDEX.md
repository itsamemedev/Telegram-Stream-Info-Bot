# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
  9969  GET              /                                                dashboard
 12016  GET              /api/abo/status                                  api_abo_status
 11970  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10757  GET              /api/automation/status                           api_automation_status
 10779  POST             /api/automation/toggle                           api_automation_toggle
 19369  GET              /api/channel/categories                          api_channel_categories
 19375  POST             /api/channel/set                                 api_channel_set
 19222  GET              /api/channels/status                             api_channels_status
 18896  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 18879  GET              /api/clips                                       api_clips
 18925  POST/DELETE      /api/clips/clear                                 api_clips_clear
 18797  GET              /api/debug/threads                               api_debug_threads
 11981  GET              /api/events                                      api_events
 11465  GET              /api/events/stream                               api_events_stream
 11292  GET              /api/health                                      api_health
 18838  POST             /api/highlights/config                           api_highlights_config
  9903  POST             /api/login                                       dashboard_login_submit
 12306  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11380  GET              /api/notify/status                               api_notify_status
 11391  POST             /api/notify/test                                 api_notify_test
 12070  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12047  GET              /api/proxy/trend                                 api_proxy_trend
 18945  GET              /api/tts/<fn>                                    api_tts_file
 19720  GET              /api/upload_window                               api_upload_window
 11582  GET              /archive/<int:eid>/download                      archive_download
 11610  GET              /download/<int:recording_id>                     download
 11539  GET              /health                                          health
 18714  GET              /healthz                                         healthz
  9894  GET              /login                                           dashboard_login_page
  9924  GET              /logout                                          dashboard_logout
  9931  GET              /manifest.webmanifest                            pwa_manifest
 19693  GET              /overlay                                         overlay_page
  9955  GET              /pwa-icon-<variant>.png                          pwa_icon
  9941  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (338)

```
   195  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   422  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   993  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   738  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   864  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   844  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   882  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   806  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   546  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   644  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1231  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1263  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   341  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   946  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   926  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1099  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1147  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1198  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1057  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   901  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   499  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   763  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   645  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   628  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   620  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   807  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   772  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   792  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   679  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   216  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   241  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   246  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   406  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   397  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   286  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   208  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   174  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   157  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   399  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
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
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   443  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   433  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   418  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   238  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   195  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    73  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    80  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   497  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   259  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   286  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   379  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   323  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   341  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   246  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
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
   112  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   120  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   136  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   200  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   220  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   247  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
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
   222  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   244  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   171  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   149  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   128  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   178  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
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
    78  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   103  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   113  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    52  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    70  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   100  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    66  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    77  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   142  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   137  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   128  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    53  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    92  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
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
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   177  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   460  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   435  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   944  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1053  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1081  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1101  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   931  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   993  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   980  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   961  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   606  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   601  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   649  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   532  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   859  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   623  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   586  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   559  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   833  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   703  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   792  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   698  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   631  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   411  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   876  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   499  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   754  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   909  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   894  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   455  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   693  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   679  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   662  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   719  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1244  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1319  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1208  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   812  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   708  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   486  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   464  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   505  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   522  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   574  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   440  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   596  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   535  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   561  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   134  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   144  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   474  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   464  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   499  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
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
   448  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   340  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   370  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
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
   238  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   453  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   482  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   402  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   415  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   511  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   388  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   263  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   308  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   332  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   319  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   165  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   277  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   135  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   369  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   424  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
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
   382  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (65)

```
  2082  /about                  Ueber diesen Bot
   809  /ai                     
  2082  /aireset                KI-Kontext zuruecksetzen
  1213  /ask                    
   910  /assign_role            
   960  /ban                    
  2037  /botstats               
  2082  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2082  /bulkadd                Mehrere User auf einmal tracken · a b c
  2082  /cleanup                Alte Aufnahmen aufraeumen
  1468  /clearwarns             
  2001  /clip                   
  1986  /clipoftheweek          
  1339  /clips                  
  2082  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
   865  /create_category        
   836  /create_channel         
   900  /create_group           
   875  /create_role            
   851  /create_voice           
  1096  /daily                  
  2082  /diag                   Vollstaendige Diagnose
  2082  /einnahmen              Einnahmen und Spenden
  1242  /event                  
  1284  /events                 
  1378  /follow                 
  1367  /help                   
   950  /kick                   
  1071  /leaderboard            
  2082  /live                   Live-Status sofort pruefen · @user
  1326  /livenow                
  2082  /logs                   Letzte Fehler aus dem Log
  2082  /pause                  Tracking pausieren · @user
  1354  /post_test              
  1174  /profile                
   982  /purge                  
  2082  /quota                  Speicher-Quota
  1058  /rank                   
  1314  /recstatus              
   920  /remove_role            
  2082  /report                 Azrael-Sentinel-Wochenreport
   822  /restream_status        
  2082  /resume                 Tracking fortsetzen · @user
   930  /set_channel_perms      
  1025  /setup_community        
  1042  /setup_targets          
  1410  /stats                  
   781  /status                 
  2082  /stoprec                Laufende Aufnahme sauber beenden · @user
  1506  /streaminfo             
  2082  /summary                Tageszusammenfassung
  2082  /sysres                 System-Ressourcen
  2082  /teststream             Recorder-Selbsttest · @user
  2082  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
   970  /timeout                
  1478  /topstreamers           
  2082  /topusers               Top-Streamer nach Aufnahmen
   711  /track                  
  2082  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   794  /tracklist              
  1392  /unfollow               
  2082  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   743  /untrack                
  1431  /warn                   
  1454  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2240  on_member_join
  2202  on_message
  2103  on_raw_reaction_add
  2275  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-456    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (46 Funktionen)

```
  1583-1634   _award_xp
  1805-1834   _clip_week_leader
  1858-1872   _clipoftheweek_loop
  2391-2453   _community_events_loop
  1540-1562   _dc_client
  1565-1574   _dc_offen
  2493-2528   _disc_automod_check
   401-406    _disc_sprache_setzen
  1637-1685   _discord_ai_automod
   534-573    _discord_automod
  1688-1708   _discord_azrael_reply
  1875-2350   _discord_run_once
   236-294    _discord_start
   297-351    _ensure_discord_invite
  2356-2388   _ensure_error_channel
   422-435    _ensure_rank_roles
   674-688    _ensure_team_roles
  2456-2486   _error_channel_loop
   583-587    _guard
   503-531    _handle_voice_ai
   409-419    _is_admin
  1753-1764   _liveboard_loop
   590-608    _on_level_up
   499-500    _par_chat_id
  1837-1855   _post_clip_of_week
  1767-1785   _post_weekly_digest
   438-464    _provision_base_channels
   467-483    _provision_user_channels
  1306-1399   _reg_betrieb
   996-1085   _reg_community_setup
  1088-1163   _reg_daily_profil
  1206-1303   _reg_frage_events
   768-824    _reg_info
   942-993    _reg_moderation
  1166-1203   _reg_profil
   891-939    _reg_rollen
   827-888    _reg_server
  1402-1489   _reg_streamer
  1492-1537   _reg_system
   702-765    _reg_tracking
   643-671    _run_tg_handler
   486-496    _tracked_usernames
   153-215    _uebernehmen
  1717-1750   _update_liveboard
  1788-1802   _weekly_digest_loop
   218-221    starte
```

## Top-Level-Symbole in bot.py (529 Funktionen, 2 Klassen)

```
 24429-24451  _abbruch_datenbank_unlesbar
  2634-2635   _abo_key
  2655-2673   _abo_probe_dump
 24544-24562  _abschluss
 15632-15639  _ad_allowlist
 16612-16618  _agent_for
 16621-16637  _ai_telemetry
 17134-17152  _alert
 20580-20630  _alert_monitor_loop
 20982-21044  _announce_loop
  3513-3523   _anthropic_key
  3530-3532   _anthropic_model
  9586-9589   _arg_int
  2626-2631   _as_dict
 24179-24188  _async_exc_handler
 17315-17337  _audio_tap_cmd
 17895-17954  _audio_tap_melden
 17351-17375  _audio_tap_sammler
  8967-9000   _aufnahme_beim_stopp_sichern
 23528-23530  _aufnahme_deckel
 24511-24531  _aufnahmen_abschliessen
 24454-24508  _aufraeumen
  9757-9826   _auth_cookie
  9724-9753   _auth_guard
  1879-1884   _auto_on
 18571-18589  _auto_restream_loop
 13486-13528  _avatar_frames_laden
 22065-22080  _azrael_broadcast_reply
 21965-21987  _azrael_chat_reply
 21937-21962  _azrael_chat_should_reply
 21993-21995  _azrael_gate_cfg
 16642-16656  _azrael_live_state
 19606-19620  _azrael_overlay_state
 17016-17070  _azrael_proactive_loop
 16460-16516  _azrael_reaction_to_chats
 21998-22005  _azrael_reply_all_chats
 21924-21934  _azrael_self_names
 22033-22062  _azrael_send_to
 13447-13483  _azrael_spricht
 16662-16683  _azrael_system
 20714-20717  _backup_active
 20795-20808  _backup_loop
 24252-24261  _brain_crowdsec_snap
 20501-20510  _brain_growth_loop
 10148-10175  _brain_growth_snapshot
  2562-2582   _brain_hint_delay
 24324-24359  _brain_moderation_snap
  6409-6437   _brain_notify
 24362-24384  _brain_recording_snap
 24264-24321  _brain_restream_health
 24387-24400  _brain_tiktok_status_snap
 11444-11461  _browser_push
  6449-6536   _build_daily_summary
 13813-13817  _build_restream_cmd
  5231-5258   _can_stop_tracking
  1992-2014   _capture_set_cookies
 12124-12127  _cfg_get
 12130-12132  _cfg_set
 19330-19365  _channel_set_all
 12675-12678  _chat_connected
 12681-12697  _chat_disconnected
  8610-8621   _chat_is_forum
 17702-17727  _chat_listener_abbauen
 12717-12719  _chat_sanitize
 12660-12672  _chat_stat
 12700-12703  _chat_stats_snapshot
  3825-3837   _check_ai_models_sync
 10430-10473  _classify_pool_anonymity
 10476-10493  _classify_pool_anonymity_bg
   875-897    _claude_chat_sync_metered
  9618-9625   _client_ip
 21128-21155  _clip_prune
 21158-21168  _clip_recfile_for
 21581-21587  _clip_should_velocity
 21210-21292  _clip_to_discord
  3711-3720   _close_ai_session
 22111-22126  _cohost_broadcast
 22096-22097  _cohost_cfg
 22152-22164  _cohost_fire_highlight
 22100-22108  _cohost_gate
 22129-22149  _cohost_highlight
 10078-10080  _conv_messages
  6808-6869   _cookie_alarm_loop
  2082-2083   _cookie_autofetch_info
  2066-2070   _cookie_autorefresh_info
 23889-23911  _cookie_bezug_loop
 23914-23939  _cookie_bezug_runde
  1969-1973   _cookie_header
  2095-2109   _cookies_selbst_holen
  4061-4073   _create_index_safe
 20052-20158  _crowdsec_status
 19998-20049  _crowdsec_via_lapi
 19902-19920  _cscli_bin
 19929-19942  _cscli_path
  6698-6723   _daily_summary_loop
 19960-19977  _darf_journal_lesen
  3047-3072   _darf_ytdlp_nachschlagen
 11625-11646  _dashboard_adresse
 20554-20577  _db_maintenance_loop
  6667-6695   _db_vacuum_loop
 15655-15679  _detect_foreign_ad
  1560-1571   _diag_path_owner
 16921-16966  _director_finalize
 17884-17891  _director_for
 16870-16918  _director_mark
 21444-21447  _disc_state_get
 21450-21457  _disc_state_set
 20482-20491  _discord_bot_starten
 20445-20456  _discord_einladung_merken
 20494-20498  _discord_invite
 20459-20479  _discord_kontext
 21405-21441  _discord_live_thread
 17073-17085  _discord_notify
 20417-20442  _discord_ops_alert
 21303-21401  _discord_post_user
 21047-21053  _discord_stop
  6726-6803   _disk_alarm_loop
 23814-23863  _disk_autoclean
 24034-24047  _disk_guard_loop
 13425-13432  _drossel_hoeher
 13421-13422  _drossel_stufe
 13435-13443  _drossel_zuruecksetzen
 11802-11804  _dump_all_threads
 10356-10419  _enrich_proxies_with_geo
  2138-2199   _ensure_cookie_file_netscape
  8669-8672   _ensure_notify_topic
 10600-10637  _ensure_proxy_ready
  8623-8650   _ensure_topic
   724-726    _env_int
   729-731    _env_int_range
 17118-17131  _event_webhook
 12475-12488  _evolution_loop
  5851-5885   _extract_file_payload
  2271-2273   _extract_urls_from_streamurl_node
 19945-19952  _f2b_sudo_hint
 24565-24628  _fatal_vom_botteil
 23533-23548  _fd_grenze_anheben
  4695-4705   _fehler_text
 10257-10275  _fetch_proxy_list
 17671-17699  _fetch_tiktok_room_id
   807-810    _ff_cmd
 13254-13259  _find_chromium
  3433-3435   _find_external_recorder
  2276-2278   _find_stream_urls
 12175-12200  _fire_webhooks
  7635-7644   _fork_safe
   908-921    _freeai_chat_sync_metered
 19991-19995  _geo_lookup_ips
  3699-3708   _get_ai_session
  7468-7508   _get_live_info
  2900-2907   _get_resolve_semaphore
  7917-8307   _handle_single_tracking
 23636-23638  _hb
 23641-23658  _hb_while
 12731-12733  _highlight_cfg
 12736-12765  _highlight_observe
 13262-13280  _htmlov_screenshot_cmd
 17377-17387  _httpx_proxy
 12208-12220  _in_quiet_hours
 24415-24426  _init_db_oder_abbruch
 25210-25241  _install_fast_eventloop
  9481-9535   _install_fast_json
 11807-11823  _install_faulthandler
 18617-18626  _intel_ensure_schema
 18669-18704  _intel_index_loop
 18638-18653  _intel_index_one
 18629-18635  _intel_semantic
  5220-5229   _is_authorized
  7818-7824   _is_dead
  2261-2263   _is_hevc
 19980-19982  _is_private_ip
  1778-1785   _is_process_running
  6439-6446   _is_quiet_hours
  1353-1362   _is_upload_window
  4560-4575   _iso
  9570-9583   _json_error_handler
  6661-6662   _kick_broadcaster_id
  6573-6615   _kick_follower_count
  6557-6560   _kick_slug
 11257-11264  _kick_user_token
 24403-24412  _kickmod_boot
  4150-4153   _kind_from_filename
 12237-12239  _latest_popularity
  1715-1724   _laufstand
 23997-24031  _laufstand_loop
 18280-18329  _live_react_loop
 17957-18269  _live_react_worker
  3283-3395   _live_status_aufloesen
 16519-16530  _live_transcript_push
 18271-18278  _live_users
 16969-17013  _living_title_loop
 20720-20792  _local_backup_scan
  9552-9566   _log_5xx
 23609-23633  _log_schleuse_pruefen
   797-804    _log_sicher
 13825-13837  _looks_like_codec_err
 13820-13822  _looks_like_source_expired
  7685-7715   _loop_fehler
 11827-11836  _loop_heartbeat
 23441-23472  _loop_lag_monitor
 23486-23506  _loop_stockung_melden
 23509-23519  _loop_takt_starten
 11839-11907  _loop_watchdog_thread
 16399-16413  _loyalty_add
 16390-16396  _loyalty_get
 16416-16424  _loyalty_top
 12347-12349  _manual_donations_total
  4902-4921   _manual_status
  7826-7827   _mark_dead
 10876-10892  _marketing_loop
 22012-22030  _maybe_handle_command
 24133-24157  _maybe_hype_clip
 21097-21125  _meme_klassifizieren
  4028-4051   _migrate_columns
 22291-22302  _mod_is_exempt
 22305-22310  _mod_warn_first
 22313-22316  _mod_warn_text
 12515-12523  _modlog
  1053-1055   _multistream_targets
  3075-3111   _nachschlag_ytdlp
  7647-7648   _nc_create_subprocess_exec
  7651-7652   _nc_create_subprocess_shell
 11194-11211  _news_loop
 12542-12544  _normalize_ingest
  2493-2510   _note_check_duration
  8663-8666   _notify_topic_name
  3114-3134   _ohne_url_melden
 16545-16553  _oracle_memories
 16819-16853  _oracle_memorize
 16556-16569  _oracle_persona
 16538-16542  _oracle_recent_text
 12888-12889  _ov_atomic_write
 12879-12881  _ov_bar
 15558-15570  _ov_clip_text
 12884-12885  _ov_oneline
 19657-19686  _overlay_push
 13208-13251  _overlay_render_size
 12611-12615  _overlay_session_reset
 19622-19624  _overlay_src_ok
 15642-15652  _own_invites
 13203-13205  _parse_size
 20166-20246  _parse_ssh_attacks
  7070-7103   _pause_resume_cmd
  2020-2064   _persist_refreshed_cookies
  1923-1955   _pick_checked_pull_proxy
  9654-9667   _pin_auth_value
  9713-9714   _pin_clear_fail
  9693-9696   _pin_locked
  9699-9710   _pin_note_fail
  9670-9690   _pin_ok
 19466-19491  _piper_pick_model
 19551-19600  _piper_say
 12137-12172  _post_json_threaded
 13182-13200  _probe_video_size
  1806-1823   _proc_is_recorder
 10569-10597  _proxy_pool_refresh_loop
  1889-1920   _proxy_report_recording
 23568-23579  _pruefung_verworfen
 11792-11794  _prune_stall_dumps
 10946-11116  _public_stats
  2086-2092   _pull_proxy_still
 17089-17115  _push_notify
  9873-9875   _pwa_dir
 10326-10341  _quick_validate_proxy
 12203-12205  _quiet_hours_config
  9838-9871   _rate_guard
 16360-16366  _react_warn
  7555-7594   _reap_proc
  8897-8964   _rec_auto_abschalten
  8844-8894   _rec_frueh_getrennt
  8727-8789   _rec_kategorie_melden
  8792-8841   _rec_totstreak_fortschreiben
  2533-2555   _record_check_outcome
   792-794    _redact_stream_urls
 10496-10566  _refresh_proxy_pool
  2310-2401   _resolve_via_html
  2680-2877   _resolve_via_webcast_api_v2
  2940-3023   _resolve_via_ytdlp
 21621-21750  _resolve_youtube_ingest
  2287-2307   _resolver_stumm
 12594-12605  _restream_active_sources
 13531-13655  _restream_avatar_feeder_start
 13658-13667  _restream_avatar_feeder_stop
 17730-17848  _restream_chat_guardian
 12768-12840  _restream_chat_push
 12865-12874  _restream_chat_push_async
 13283-13392  _restream_html_overlay_start
 13395-13408  _restream_html_overlay_stop
 12553-12576  _restream_overlay_files
 18333-18365  _restream_platform_state
 18533-18568  _restream_resume_after_restart
 13715-13779  _restream_tts_enqueue_wav
 13144-13176  _restream_tts_feeder
 13141-13142  _restream_tts_fifo_path
 13670-13697  _restream_tts_start
 13699-13713  _restream_tts_stop
 18371-18530  _restream_verify_loop
 20685-20697  _retention_loop
 20679-20682  _retention_scan
  2637-2639   _room_is_abo
  5889-6006   _run_ai_call
 11930-11943  _run_async_from_flask
 19985-19988  _run_priv
 25198-25206  _run_selfcheck_and_exit
 20700-20711  _s3_client
  7853-7904   _safe_send
  4828-4844   _sample_net_throughput
  2585-2612   _schedule_next_check
 20633-20676  _scheduler_loop
  4054-4058   _schema_pk
 11947-11952  _scraper_session
 22319-22358  _screen_full
 11308-11345  _sec_headers
  2266-2268   _select_stream_from_data_section
 24918-25195  _selfcheck
  8675-8709   _send_live_notice
  1376-1380   _should_defer_upload
 21171-21207  _shrink_for_discord
  9878-9890   _sicheres_ziel
 20513-20551  _sicherheits_erinnerung_loop
 24054-24071  _sign_health_check
 24074-24093  _sign_health_loop
  4578-4603   _sitzung_bestimmen
  7664-7675   _spawn
 25623-25653  _spawn_from_flask
 23582-23588  _speicher_maps
 23591-23606  _speicher_pflegen
 17389-17668  _start_chat_listener
 23551-23565  _start_gesperrt
 11910-11927  _start_loop_watchdog
 11143-11189  _stats_loop
 11122-11125  _stats_output_path
 11128-11140  _stats_write
 19503-19517  _stimme_saubern
 19524-19548  _stimme_schon_gesagt
  8386-8402   _storage_cleanup_loop
 24113-24120  _story_for
  3458-3464   _stream_url_expiry
  3466-3471   _stream_url_ttl
 15605-15612  _streamer_persona_get
 20817-20939  _system_backup
 20948-20978  _system_backup_loop
 11752-11770  _task_auf_bot_schleife
 23132-23148  _telegram_befehlsmenue
  7718-7764   _telegram_polling_fehler
 10278-10317  _test_proxy
 10824-10840  _testpush_resolve_live
  7829-7850   _tg_sprache_setzen
  8582-8592   _tg_topics_load_into_mem
  8579-8580   _tg_topics_path
  8594-8601   _tg_topics_save
  9628-9636   _token_ok
  8604-8608   _topic_forget
 12223-12234  _tracking_max_duration
  4358-4372   _tracking_remove_cleanup
  4389-4401   _tracking_resume_cleanup
  1618-1641   _try_attach_file_handler
 19493-19501  _tts_cleanup
 10800-10804  _tunnel_effective
 23866-23886  _tunnel_lage
 23942-23994  _tunnel_wacht_loop
 18989-19042  _twitch_channel_status
 22361-22506  _twitch_chat_loop
 21463-21476  _twitch_clip_versuchen
 22175-22278  _twitch_eventsub_loop
  1399-1412   _upload_queue_add
  1423-1425   _upload_queue_count
  1382-1391   _upload_queue_load
  1372-1374   _upload_queue_path
  1414-1421   _upload_queue_remove
  1393-1397   _upload_queue_save
  1427-1468   _upload_window_loop
  7528-7535   _uptime_s
 12530-12539  _url_host
  3137-3231   _url_nachschlag
   868-872    _usage_record_claude
 24227-24249  _v37_pause_source
 24191-24201  _v37_restream_restart
 24204-24224  _v37_unpause_source
  7767-7811   _verbindung_verloren
  6618-6649   _viewer_sample_loop
  9717-9720   _wants_html
  7538-7552   _warn_empty_env
 23679-23800  _watchdog_loop
 21896-21904  _wchat_thank_ok
 17157-17187  _whisper_get_model
  7625-7632   _whisper_native_section
 16347-16353  _whisper_pool
 17281-17313  _whisper_segments
 17189-17205  _whisper_stumm
 17208-17278  _whisper_transcribe
 12936-13098  _write_restream_overlay
 12898-12933  _write_restream_overlay_async
 22530-22626  _youtube_api_chat_loop
 19045-19148  _youtube_api_status
 19151-19218  _youtube_channel_status
 22629-22790  _youtube_chat_loop
 21479-21504  _youtube_clip_versuchen
 21756-21769  _youtube_restream_autoconfig
 21772-21796  _youtube_restream_autoconfig_inner
 21863-21891  _youtube_send
 19286-19327  _youtube_set_channel
 21799-21833  _yt_access_token
 21836-21851  _yt_live_chat_id
 21859-21860  _yt_sendrate_cfg
 22509-22524  _yt_timeout
  2924-2925   _ytdlp_detect_available
  2927-2938   _ytdlp_note_result
 11797-11799  _zombie_child_count
  7404-7428   about
  4269-4273   add_ai_log_entry
  4186-4189   add_archive_entry
  4866-4868   add_archive_rule
  4606-4677   add_recording
  4333-4350   add_tracking
  6009-6042   ai
  3851-3932   ai_chat
  3966-3976   ai_history_append
  3978-3983   ai_history_clear
  3955-3964   ai_history_load
  3940-3953   ai_rate_limit_check
  6071-6079   aireset
 16686-16705  azrael_chat
 22795-22917  brain_cmd
  3474-3479   build_recording_cmd
  4353-4356   bulk_add_trackings
  6872-6931   bulkadd
  8405-8562   check_all_trackings
  4405-4417   claim_live_transition
 15682-16279  class KickModerator
 13840-15445  class RestreamManager
 10683-10725  classify_proxy_anonymity
  6117-6315   cleanup
  5156-5162   cleanup_old_recordings
  4551-4558   clear_recording
 21507-21578  clip_moment
  4818-4821   compute_storage_forecast
  6994-7067   cookies_cmd
  4324-4330   count_trackings_for_chat
  4256-4267   decide_preferred_recorder
  4196-4199   delete_archive_entry
  4870-4872   delete_archive_rule
  5546-5693   diag
 23029-23090  einnahmen_cmd
  4812-4815   find_recordings_by_fingerprint
  4217-4233   finish_recording_attempt
  4377-4379   get_all_active_trackings
  4284-4286   get_all_checks
  4679-4682   get_all_recordings
  4761-4763   get_all_tags_with_counts
  4789-4792   get_annotations_for_recording
  4191-4194   get_archive_entry
  4782-4785   get_bookmarked_recordings
  2126-2131   get_cookie_health
  4749-4755   get_event_log
  4240-4254   get_last_recording_attempt
  3234-3276   get_live_status
  5095-5098   get_manual_recordings
  4797-4800   get_or_compute_inspect_sync
  5197-5200   get_outcome_breakdown
  4768-4771   get_priority_poll_interval
  4235-4238   get_recent_recording_attempts
  4684-4687   get_recording_by_id
  4775-4778   get_recording_note
  3645-3668   get_redis
  4313-4316   get_stats
  5150-5154   get_storage_stats
  4890-4892   get_tiktok_status_distribution
  4419-4428   get_tracking_state
  4374-4375   get_trackings_for_group
  5111-5114   get_trash_recordings
  9003-9460   handle_recording_finished
 23124-23129  hilfe_cmd
  4081-4141   init_db
  4862-4864   list_archive_rules
  5350-5388   live
  7907-7915   live_check_worker
  3723-3762   llm_chat
  3785-3815   llm_chat_sync
  3770-3782   llm_list_models
  4708-4741   log_event
  1740-1773   log_recording_failure
  7217-7266   logs_cmd
 24631-24908  main
  6045-6068   on_ai_media
  7343-7369   on_ai_reply
  7372-7401   on_azrael_mention
  7433-7463   on_callback
 16711-16816  oracle_handle
  7106-7109   pause_tracking
  5210-5215   profile_keyboard
  7168-7214   quota
  8309-8383   reaper_loop
  4886-4888   record_tiktok_status
  6084-6114   recstatus
  3670-3678   redis_get_json
  3681-3687   redis_set_json
 23151-23161  report_cmd
 10728-10730  report_proxy_result
  2404-2446   resolve_tiktok_live_stream
  5106-5109   restore_recording
  7112-7115   resume_tracking
  4875-4880   run_archive_rules
 23164-23421  run_bot
 11649-11743  run_flask
  4850-4853   sample_bandwidth_for_active
  4276-4282   save_tiktok_check
  4543-4549   set_recording_file
  4382-4386   set_tracking_paused
  5101-5104   soft_delete_recording
  8715-8725   split_and_send_video
  5263-5305   start
  4201-4215   start_recording_attempt
  6318-6356   stats
  5040-5093   stop_manual_recording
  7118-7165   stoprec
  6542-6550   summary_cmd
  7269-7340   sysres
  5695-5839   teststream
  5307-5348   tiktok
  6934-6991   topusers
  5425-5482   track
  5390-5422   track_exact
  5496-5544   tracklist
  4924-5038   trigger_manual_recording
  4504-4541   try_acquire_recording_lock
  5117-5119   universal_search
 23093-23121  unpause_cmd
  5484-5494   untrack
 22920-23026  update_cmd
  4807-4810   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, run_archive_file_check, uebernehmen
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, concat_cmd, concat_liste, gehoert_dazu, luecken, sekunden, sitzung_id, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
befehle.py             beschreibung, discord_nativ, discord_ueber_tg, fuer, hilfe_text, pruefen, telegram_handler
betriebslage.py        bereit, bewerten, sichern_beim_stopp
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
cookieholen.py         aktualisiere, aus_browser, configure, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, gesundheit, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, set_pool
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      anzeige_groesse, avatar_kette, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
gegendruck.py          abgewiesen, deckel_auto, fd_grenze_anheben, fd_lage, freigeben, lage, reservieren, reserviert, start_entscheiden, verworfen, zuruecksetzen
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, configure, oauth_exchange, search_category, send_message, slug, timeout_user, update_channel, user_token
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              backend, lokal_stand, lokal_zuerst, normal, provider
lagebild.py            bauen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, setzen, statistik, zaehle, zaehler_zuruecksetzen
livefolge.py           braucht_url_nachschlag, hat_stream_url, last_dehnung, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, entkoppeln, nachziehen, stoppen, synchrone_handler, verloren, wartend, zuruecksetzen
looplag.py             bremser, erfassen, lage, spaeher_starten, stelle_aus_rahmen, takt, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
meldetakt.py           melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, quelle_lage, quelle_laut, text
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, schriftart
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              create_schema
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
speicherpflege.py      abgelaufene_weg, alte_stempel_weg, groessen
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, forecast, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
telegramfehler.py      dauer_text, grund, ist_fehler, text, zuruecksetzen
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, garantie, garantie_cmd, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlpurl.py            urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
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
